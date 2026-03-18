# OpenClaw 部署说明

这个仓库提供了一个一键部署（源码编译）OpenClaw 的脚本。

## 1. 依赖

以 Ubuntu/Debian 为例：

```bash
sudo apt update
sudo apt install -y git cmake build-essential libsdl2-dev libsdl2-mixer-dev libsdl2-image-dev zlib1g-dev
```

> 说明：OpenClaw 是桌面游戏项目，不是常驻 Web 服务。通常做法是编译并在图形环境中运行。

## 2. 一键部署

```bash
./scripts/deploy_openclaw.sh
```

默认行为：

- 拉取源码：`https://github.com/pjasicek/OpenClaw.git`
- 构建目录：`./openclaw-src/build`
- 安装目录：`./openclaw-src/dist`

## 3. 可选环境变量

你可以通过环境变量自定义部署参数：

```bash
OPENCLAW_REPO_URL=https://github.com/pjasicek/OpenClaw.git \
OPENCLAW_REPO_DIR=./openclaw-src \
OPENCLAW_BUILD_DIR=./openclaw-src/build \
OPENCLAW_INSTALL_PREFIX=./openclaw-src/dist \
OPENCLAW_JOBS=8 \
./scripts/deploy_openclaw.sh
```

## 4. 启动

编译安装完成后，可执行文件通常在：

```bash
./openclaw-src/dist/bin/OpenClaw
```

如果你在服务器环境（无桌面）部署，请使用 X11 转发、VNC 或虚拟显示环境（如 Xvfb）。

---

## 5. 物体识别系统（新增）

仓库新增了一个基于 OpenCV 的物体识别示例，目录：

- `object_recognition/detect.py`
- `object_recognition/README.md`

快速开始：

```bash
pip install -r object_recognition/requirements.txt
python object_recognition/detect.py --source 0
```
