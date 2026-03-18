#!/usr/bin/env python3
"""简单的物体识别系统（基于 OpenCV DNN + MobileNet-SSD）。"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from urllib.request import urlretrieve

import cv2
import numpy as np

MODEL_DIR = Path(__file__).resolve().parent / "models"
PROTOTXT = MODEL_DIR / "MobileNetSSD_deploy.prototxt"
MODEL = MODEL_DIR / "MobileNetSSD_deploy.caffemodel"

PROTOTXT_URL = (
    "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/"
    "MobileNetSSD_deploy.prototxt"
)
MODEL_URL = (
    "https://github.com/chuanqi305/MobileNet-SSD/raw/master/"
    "MobileNetSSD_deploy.caffemodel"
)

CLASSES = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
]


def ensure_model_files() -> None:
    """如果模型文件不存在则自动下载。"""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if not PROTOTXT.exists():
        print(f"[INFO] 下载网络结构文件: {PROTOTXT}")
        urlretrieve(PROTOTXT_URL, PROTOTXT)

    if not MODEL.exists():
        print(f"[INFO] 下载模型权重文件: {MODEL}")
        urlretrieve(MODEL_URL, MODEL)


def parse_source(source: str) -> str | int:
    """将输入源解析为摄像头索引或文件路径。"""
    return int(source) if source.isdigit() else source


def detect_on_frame(frame: np.ndarray, net: cv2.dnn_Net, confidence: float) -> np.ndarray:
    """在单帧图像上执行检测并绘制结果。"""
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)),
        scalefactor=0.007843,
        size=(300, 300),
        mean=127.5,
    )

    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        conf = float(detections[0, 0, i, 2])
        if conf < confidence:
            continue

        class_id = int(detections[0, 0, i, 1])
        if class_id >= len(CLASSES):
            label = f"unknown-{class_id}"
        else:
            label = CLASSES[class_id]

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label}: {conf * 100:.1f}%"
        text_y = y1 - 8 if y1 - 8 > 10 else y1 + 20
        cv2.putText(
            frame,
            text,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

    return frame


def run_image_mode(image_path: Path, net: cv2.dnn_Net, confidence: float, output: Path | None) -> None:
    frame = cv2.imread(str(image_path))
    if frame is None:
        raise FileNotFoundError(f"无法读取图片: {image_path}")

    result = detect_on_frame(frame, net, confidence)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), result)
        print(f"[INFO] 检测结果已保存: {output}")

    cv2.imshow("Object Recognition", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_video_mode(source: str | int, net: cv2.dnn_Net, confidence: float, output: Path | None) -> None:
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频源: {source}")

    writer = None
    fps_start = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        result = detect_on_frame(frame, net, confidence)

        elapsed = max(time.time() - fps_start, 1e-9)
        fps = frame_count / elapsed
        cv2.putText(
            result,
            f"FPS: {fps:.2f}",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        if output and writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            h, w = result.shape[:2]
            writer = cv2.VideoWriter(str(output), fourcc, 25.0, (w, h))

        if writer:
            writer.write(result)

        cv2.imshow("Object Recognition", result)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break

    cap.release()
    if writer:
        writer.release()
        print(f"[INFO] 视频检测结果已保存: {output}")
    cv2.destroyAllWindows()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="简单物体识别系统")
    parser.add_argument(
        "--source",
        default="0",
        help="输入源：摄像头编号(默认 0)、视频文件路径或图片路径",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.4,
        help="置信度阈值，默认 0.4",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=None,
        help="保存检测结果到文件（图片/视频）",
    )
    return parser


def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    ensure_model_files()
    net = cv2.dnn.readNetFromCaffe(str(PROTOTXT), str(MODEL))

    source_value = args.source
    source_path = Path(source_value)

    if source_path.exists() and is_image_file(source_path):
        run_image_mode(source_path, net, args.confidence, args.save)
    else:
        source = parse_source(source_value)
        run_video_mode(source, net, args.confidence, args.save)


if __name__ == "__main__":
    main()
