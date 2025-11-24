import cv2
import numpy as np
from ultralytics import YOLO
import os

# ---------------- Load YOLOv8 Model ----------------
# Make sure 'hazard_model.pt' is in your project root
MODEL_PATH = "hazard_model.pt"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found! Train the model first using train_hazard_model.py")

model = YOLO(MODEL_PATH)

# ---------------- Hazard Classes ----------------
HAZARD_CLASSES = ["gas_cylinder", "electrical_fire", "industrial_fire", "ppe"]

# ---------------- Detection Function ----------------
def detect_hazards_with_boxes(frame):
    """
    Detect hazards in an image/frame and draw bounding boxes.
    Returns:
        frame with bounding boxes,
        list of detected hazard class names
    """
    if isinstance(frame, np.ndarray):
        img = frame.copy()
    else:
        img = np.array(frame)

    detected_hazards = []

    results = model.predict(img, imgsz=640, conf=0.4)  # Adjust confidence threshold

    for result in results:
        boxes = result.boxes
        for box, cls in zip(boxes.xyxy, boxes.cls):
            cls = int(cls)
            if cls < len(HAZARD_CLASSES):
                label = HAZARD_CLASSES[cls]
                detected_hazards.append(label)

                # Draw bounding box
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

    detected_hazards = list(set(detected_hazards))  # Remove duplicates
    return img, detected_hazards

