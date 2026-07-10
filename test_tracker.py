from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(
    source="videos/traffic.mp4",
    tracker="bytetrack.yaml",
    stream=True,
    persist=True,
    verbose=False
)

count = 0

for r in results:
    count += 1

print("Tracking Working!")
print("Frames Processed:", count)