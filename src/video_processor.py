"""
TrafficVision AI
Video Processing Module
"""

import cv2

from src.tracker import TrafficTracker


class VideoProcessor:

    def __init__(self):

        self.tracker = TrafficTracker()

        self.frame_number = 0

    def process_frame(self, frame):
        """
        Process a single frame.

        Returns:
            annotated_frame
            tracked_data
        """

        self.frame_number += 1

        annotated_frame, tracked_data = self.tracker.track(frame)

        return annotated_frame, tracked_data

    def process_video(self, video_path):
        """
        Process an entire video for standalone testing.
        Press 'q' to quit.
        """

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Unable to open video: {video_path}")
            return

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            annotated_frame, tracked_data = self.process_frame(frame)

            cv2.imshow(
                "TrafficVision AI",
                annotated_frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cap.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":

    processor = VideoProcessor()

    processor.process_video(
        "data/inputs/sample.mp4"
    )