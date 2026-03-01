#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${OPENCLAW_REPO_URL:-https://github.com/pjasicek/OpenClaw.git}"
REPO_DIR="${OPENCLAW_REPO_DIR:-./openclaw-src}"
BUILD_DIR="${OPENCLAW_BUILD_DIR:-${REPO_DIR}/build}"
INSTALL_PREFIX="${OPENCLAW_INSTALL_PREFIX:-${REPO_DIR}/dist}"
JOBS="${OPENCLAW_JOBS:-$(nproc)}"

printf '>>> OpenClaw source: %s\n' "$REPO_URL"
printf '>>> Workdir: %s\n' "$REPO_DIR"

if [ ! -d "$REPO_DIR/.git" ]; then
  git clone "$REPO_URL" "$REPO_DIR"
else
  git -C "$REPO_DIR" pull --ff-only
fi

cmake -S "$REPO_DIR" -B "$BUILD_DIR" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX"

cmake --build "$BUILD_DIR" --parallel "$JOBS"
cmake --install "$BUILD_DIR"

cat <<MSG

OpenClaw 已完成编译安装。

可执行文件通常位于：
  ${INSTALL_PREFIX}/bin

如果你准备在图形桌面环境运行，可以执行：
  ${INSTALL_PREFIX}/bin/OpenClaw

MSG
