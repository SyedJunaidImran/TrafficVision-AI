"""
TrafficVision AI
Tracker Module

Tracks vehicles using YOLOv8 + ByteTrack.
"""

import cv2
from ultralytics import YOLO


class TrafficTracker:
    """
    Vehicle tracking using YOLOv8 + ByteTrack.
    """

    def __init__(
        self,
        model_path="models/yolov8n.pt",
        confidence=0.35
    ):

        self.model = YOLO(model_path)

        self.confidence = confidence

        # COCO vehicle classes
        self.vehicle_classes = {
            2: "Car",
            3: "Motorcycle",
            5: "Bus",
            7: "Truck"
        }

        # Latest tracked objects
        self.tracked_objects = {}
    def track(self, frame):
        """
        Track vehicles using YOLOv8 + ByteTrack.

        Parameters:
            frame (numpy.ndarray)

        Returns:
            annotated_frame
            tracked_data
        """

        results = self.model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=self.confidence,
            verbose=False
        )

        result = results[0]

        annotated_frame = frame.copy()

        tracked_data = []

        # No detections
        if result.boxes is None:
            return annotated_frame, tracked_data

        boxes = result.boxes

        for box in boxes:

            # Skip objects without IDs
            if box.id is None:
                continue

            track_id = int(box.id.item())

            cls = int(box.cls.item())

            if cls not in self.vehicle_classes:
                continue

            confidence = float(box.conf.item())

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            class_name = self.vehicle_classes[cls]

            vehicle = {
                "id": track_id,
                "class": class_name,
                "confidence": confidence,
                "bbox": (
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2)
                ),
                "center": (
                    center_x,
                    center_y
                )
            }

            tracked_data.append(vehicle)

            # Save latest tracked object
            self.tracked_objects[track_id] = {
                "center": (
                    center_x,
                    center_y
                ),
                "class": class_name
            }
                        # Draw bounding box
            cv2.rectangle(
                annotated_frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            # Draw center point
            cv2.circle(
                annotated_frame,
                (center_x, center_y),
                4,
                (0, 0, 255),
                -1
            )

            # Display tracking ID and class
            label = (
                f"{class_name} "
                f"ID:{track_id}"
            )

            cv2.putText(
                annotated_frame,
                label,
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

        return annotated_frame, tracked_data
    def get_tracked_objects(self):
        """
        Returns the latest tracked objects.
        """

        return self.tracked_objects.copy()


    def reset(self):
        """
        Clears all tracked objects.
        Useful when processing a new video.
        """

        self.tracked_objects.clear()


if __name__ == "__main__":

    video_path = "data/inputs/sample.mp4"

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Unable to open video: {video_path}")
        exit()

    tracker = TrafficTracker()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        annotated_frame, tracked_data = tracker.track(frame)

        cv2.imshow(
            "TrafficVision AI Tracker",
            annotated_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()

    print("Tracking completed successfully.")