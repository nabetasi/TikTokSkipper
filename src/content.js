(() => {
  "use strict";

  const STEP = 1;
  const ROOT_ID = "tiktok-skipper-root";

  /** @type {HTMLVideoElement | null} */
  let activeVideo = null;
  /** @type {Map<Element, number>} */
  const intersectionRatio = new Map();
  let rafScheduled = false;

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  function scoreVideo(video) {
    const rect = video.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) return -1;

    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const cx = vw / 2;
    const cy = vh / 2;
    const vcx = rect.left + rect.width / 2;
    const vcy = rect.top + rect.height / 2;
    const dist = Math.hypot(vcx - cx, vcy - cy);

    const visibleW =
      clamp(rect.right, 0, vw) - clamp(rect.left, 0, vw);
    const visibleH =
      clamp(rect.bottom, 0, vh) - clamp(rect.top, 0, vh);
    const visibleArea = Math.max(0, visibleW) * Math.max(0, visibleH);
    const io = intersectionRatio.get(video) ?? 0;

    const playing = !video.paused && !video.ended ? 1 : 0;
    const ready =
      typeof video.readyState === "number" && video.readyState >= 2 ? 1 : 0;

    return (
      playing * 5e6 +
      ready * 1e5 +
      io * 1e4 +
      visibleArea -
      dist * 8
    );
  }

  function pickActiveVideo() {
    const videos = document.querySelectorAll("video");
    let best = null;
    let bestScore = -Infinity;
    videos.forEach((v) => {
      const s = scoreVideo(v);
      if (s > bestScore) {
        bestScore = s;
        best = v;
      }
    });
    activeVideo = bestScore > 0 ? best : null;
  }

  function scheduleUpdate() {
    if (rafScheduled) return;
    rafScheduled = true;
    requestAnimationFrame(() => {
      rafScheduled = false;
      pickActiveVideo();
    });
  }

  const intersectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        intersectionRatio.set(e.target, e.intersectionRatio);
      });
      scheduleUpdate();
    },
    { threshold: [0, 0.1, 0.25, 0.5, 0.75, 1] }
  );

  const observed = new WeakSet();

  function observeVideo(video) {
    if (observed.has(video)) return;
    observed.add(video);
    intersectionObserver.observe(video);
    ["play", "playing", "pause", "seeked", "loadeddata", "emptied"].forEach(
      (ev) => {
        video.addEventListener(ev, scheduleUpdate, { passive: true });
      }
    );
  }

  function scanVideos() {
    document.querySelectorAll("video").forEach(observeVideo);
    scheduleUpdate();
  }

  const mutationObserver = new MutationObserver(() => {
    scanVideos();
  });

  function ensureUi() {
    let root = document.getElementById(ROOT_ID);
    if (root) return root;

    root = document.createElement("div");
    root.id = ROOT_ID;
    root.setAttribute("role", "toolbar");
    root.setAttribute("aria-label", "TikTok Skipper");

    const back = document.createElement("button");
    back.type = "button";
    back.className = "tiktok-skipper-btn";
    back.textContent = "−1秒";
    back.setAttribute("aria-label", "1秒戻す");

    const fwd = document.createElement("button");
    fwd.type = "button";
    fwd.className = "tiktok-skipper-btn";
    fwd.textContent = "+1秒";
    fwd.setAttribute("aria-label", "1秒送る");

    const toast = document.createElement("div");
    toast.className = "tiktok-skipper-toast";
    toast.setAttribute("aria-live", "polite");

    let toastTimer = 0;
    function showToast(message) {
      toast.textContent = message;
      toast.classList.add("tiktok-skipper-toast--show");
      window.clearTimeout(toastTimer);
      toastTimer = window.setTimeout(() => {
        toast.classList.remove("tiktok-skipper-toast--show");
      }, 1600);
    }

    function seek(delta) {
      pickActiveVideo();
      const v = activeVideo;
      if (!v) {
        showToast("操作できる動画が見つかりません。");
        return;
      }
      const d =
        typeof v.duration === "number" && Number.isFinite(v.duration)
          ? v.duration
          : null;
      const cur = v.currentTime;
      let next = cur + delta;
      if (d != null) next = clamp(next, 0, d);
      else next = Math.max(0, next);
      try {
        v.currentTime = next;
      } catch {
        showToast("シークできませんでした。");
      }
    }

    back.addEventListener("click", () => seek(-STEP));
    fwd.addEventListener("click", () => seek(STEP));

    root.appendChild(back);
    root.appendChild(fwd);
    document.documentElement.appendChild(root);
    document.documentElement.appendChild(toast);

    return root;
  }

  function init() {
    ensureUi();
    scanVideos();
    mutationObserver.observe(document.documentElement, {
      childList: true,
      subtree: true,
    });
    window.addEventListener("resize", scheduleUpdate, { passive: true });
    window.addEventListener("scroll", scheduleUpdate, {
      passive: true,
      capture: true,
    });
    window.setInterval(() => {
      pickActiveVideo();
    }, 700);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
