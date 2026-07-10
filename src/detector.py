"""
TrafficVision AI
Detector Module

YOLOv8 Object Detection
Author: Junaid
"""

from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path


class TrafficDetector:
    """
    Wrapper class around Ultralytics YOLO model.
    """

    def __init__(
        self,
        model_path: str = "models/yolov8n.pt",
        confidence: float = 0.35,
        device: str = "cpu",
    ):
        self.model_path = model_path
        self.confidence = confidence
        self.device = device

        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"YOLO model not found: {model_path}"
            )

        self.model = YOLO(model_path)

        self.vehicle_classes = {
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck",
        }

    def detect(self, frame):
        """
        Detect vehicles in a frame.

        Returns:
            boxes
            confidences
            class_ids
            class_names
            annotated_frame
        """

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            verbose=False,
            device=self.device,
        )

        annotated = frame.copy()

        boxes = []
        confidences = []
        class_ids = []
        class_names = []

        result = results[0]

        if result.boxes is None:
            return (
                boxes,
                confidences,
                class_ids,
                class_names,
                annotated,
            )

        for box in result.boxes:

            cls = int(box.cls.item())

            if cls not in self.vehicle_classes:
                continue

            confidence = float(box.conf.item())

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            boxes.append(
                [
                    float(x1),
                    float(y1),
                    float(x2),
                    float(y2),
                ]
            )

            confidences.append(confidence)
            class_ids.append(cls)
            class_names.append(self.vehicle_classes[cls])

            cv2.rectangle(
                annotated,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2,
            )

            label = (
                f"{self.vehicle_classes[cls]} "
                f"{confidence:.2f}"
            )

            cv2.putText(
                annotated,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2,
            )

        return (
            boxes,
            confidences,
            class_ids,
            class_names,
            annotated,
        )

    def detect_with_tracking(self, frame):
        """
        Runs YOLOv8 with built-in ByteTrack.

        Returns:
            Ultralytics tracking result.
        """

        results = self.model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=self.confidence,
            verbose=False,
            device=self.device,
        )

        return results[0]


if __name__ == "__main__":

    detector = TrafficDetector()

    cap = cv2.VideoCapture("sample.mp4")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        _, _, _, _, output = detector.detect(frame)

        cv2.imshow("TrafficVision AI Detector", output)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()