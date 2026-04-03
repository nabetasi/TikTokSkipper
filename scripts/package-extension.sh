#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${ROOT}/build"
ZIP_NAME="tiktok-skipper-chrome-store-v1.0.0.zip"
mkdir -p "${OUT_DIR}"
(
  cd "${ROOT}"
  zip -r "${OUT_DIR}/${ZIP_NAME}" \
    manifest.json \
    src \
    icons \
    -x "*.DS_Store"
)
echo "Created ${OUT_DIR}/${ZIP_NAME}"
