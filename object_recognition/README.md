# 物体识别系统

这是一个可直接运行的轻量级物体识别系统，基于 **OpenCV DNN + MobileNet-SSD**。

## 功能

- 支持摄像头实时识别（默认 `--source 0`）
- 支持视频文件识别
- 支持单张图片识别
- 自动下载模型文件（首次运行）
- 可选保存结果到本地文件

## 支持类别

模型支持 20 类常见对象：

`aeroplane, bicycle, bird, boat, bottle, bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, pottedplant, sheep, sofa, train, tvmonitor`

## 安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r object_recognition/requirements.txt
```

## 使用方式

### 1) 摄像头实时识别

```bash
python object_recognition/detect.py --source 0
```

### 2) 视频文件识别

```bash
python object_recognition/detect.py --source /path/to/video.mp4 --save output/result.mp4
```

### 3) 单张图片识别

```bash
python object_recognition/detect.py --source /path/to/image.jpg --save output/result.jpg
```

### 关键参数

- `--source`：输入源（摄像头编号 / 视频路径 / 图片路径）
- `--confidence`：置信度阈值，默认 `0.4`
- `--save`：检测结果保存路径（可选）

## 退出方式

视频模式下按 `q` 或 `ESC` 退出。
