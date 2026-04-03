(() => {
  "use strict";

  const ROOT_ID = "tiktok-skipper-root";
  const SCAN_DEBOUNCE_MS = 40;

  /** @type {HTMLVideoElement | null} */
  let activeVideo = null;
  /** @type {Map<Element, number>} */
  const intersectionRatio = new Map();
  let rafScheduled = false;
  /** @type {number | null} */
  let scanTimer = null;
  /** @type {HTMLVideoElement[]} */
  let cachedVideos = [];

  function clamp(n, min, max) {
    return Math.min(max, Math.max(min, n));
  }

  /**
   * TikTok はプレイヤーを Shadow DOM に置くことがあるため、子孫と shadow root を走査する。
   * @param {Node} node
   * @param {HTMLVideoElement[]} out
   */
  function collectVideosDeep(node, out) {
    if (!node) return;
    if (node.nodeName === "VIDEO" && node instanceof HTMLVideoElement) {
      out.push(node);
    }
    if (node instanceof Element && node.shadowRoot) {
      collectVideosDeep(node.shadowRoot, out);
    }
    const children = node.childNodes;
    for (let i = 0; i < children.length; i++) {
      collectVideosDeep(children[i], out);
    }
  }

  /** @returns {HTMLVideoElement[]} */
  function getAllVideos() {
    const out = [];
    collectVideosDeep(document.documentElement, out);
    return out;
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
    const videos =
      cachedVideos.length > 0
        ? cachedVideos
        : getAllVideos();
    let best = null;
    let bestScore = -Infinity;
    videos.forEach((v) => {
      if (!v.isConnected) return;
      const s = scoreVideo(v);
      if (s > bestScore) {
        bestScore = s;
        best = v;
      } else if (s === bestScore && s > -1 && best != null) {
        const tieBreak =
          (intersectionRatio.get(v) ?? 0) -
          (intersectionRatio.get(best) ?? 0);
        if (tieBreak > 0) best = v;
      }
    });
    activeVideo = bestScore > -1 && best != null ? best : null;
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
    cachedVideos = getAllVideos();
    cachedVideos.forEach(observeVideo);
    scheduleUpdate();
  }

  function scheduleScan() {
    if (scanTimer != null) window.clearTimeout(scanTimer);
    scanTimer = window.setTimeout(() => {
      scanTimer = null;
      scanVideos();
    }, SCAN_DEBOUNCE_MS);
  }

  const mutationObserver = new MutationObserver(() => {
    scheduleScan();
  });

  function ensureUi() {
    let root = document.getElementById(ROOT_ID);
    if (root) return root;

    root = document.createElement("div");
    root.id = ROOT_ID;
    root.setAttribute("role", "toolbar");
    root.setAttribute("aria-label", "TikTok Skipper");

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
        showToast("No video found.");
        return;
      }
      if (v.readyState < 1) {
        showToast("Waiting for video to load.");
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
        showToast("Seek failed.");
      }
    }

    function makeSeekButton(label, ariaLabel, delta) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "tiktok-skipper-btn";
      btn.textContent = label;
      btn.setAttribute("aria-label", ariaLabel);
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        seek(delta);
      });
      btn.addEventListener(
        "pointerdown",
        (ev) => {
          ev.stopPropagation();
        },
        true
      );
      return btn;
    }

    const row1 = document.createElement("div");
    row1.className = "tiktok-skipper-row";
    row1.appendChild(
      makeSeekButton("−1s", "Seek back 1 second", -1)
    );
    row1.appendChild(
      makeSeekButton("+1s", "Seek forward 1 second", 1)
    );

    const row2 = document.createElement("div");
    row2.className = "tiktok-skipper-row";
    row2.appendChild(
      makeSeekButton("−0.5s", "Seek back 0.5 seconds", -0.5)
    );
    row2.appendChild(
      makeSeekButton("+0.5s", "Seek forward 0.5 seconds", 0.5)
    );

    root.appendChild(row1);
    root.appendChild(row2);
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
      scanVideos();
    }, 700);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
