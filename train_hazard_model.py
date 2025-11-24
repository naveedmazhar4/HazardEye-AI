import os
import cv2
import numpy as np
from ultralytics import YOLO

# ==============================================================
# 1. CREATE FOLDER STRUCTURE
# ==============================================================

os.makedirs("dataset/images/train", exist_ok=True)
os.makedirs("dataset/images/val", exist_ok=True)
os.makedirs("dataset/labels/train", exist_ok=True)
os.makedirs("dataset/labels/val", exist_ok=True)

CLASSES = ["gas_cylinder", "electrical_fire", "industrial_fire", "ppe"]

# ==============================================================
# 2. GENERATE SYNTHETIC TRAINING DATA (50 images per class)
# ==============================================================

def generate_dummy_image(label_index, img_path, label_path):
    img = np.zeros((640, 640, 3), dtype=np.uint8)

    # Draw a colored rectangle
    x1, y1, x2, y2 = 150, 150, 450, 450
    color = (0, 255, 0)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 4)

    cv2.putText(img, CLASSES[label_index], (160, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

    cv2.imwrite(img_path, img)

    # YOLO normalized label
    x_center = (x1 + x2) / 2 / 640
    y_center = (y1 + y2) / 2 / 640
    width = (x2 - x1) / 640
    height = (y2 - y1) / 640

    with open(label_path, "w") as f:
        f.write(f"{label_index} {x_center} {y_center} {width} {height}")


print("\n📌 Generating dummy dataset...")
for i, cls in enumerate(CLASSES):
    for img_num in range(50):
        prefix = "train" if img_num < 40 else "val"
        img_path = f"dataset/images/{prefix}/{cls}_{img_num}.jpg"
        label_path = f"dataset/labels/{prefix}/{cls}_{img_num}.txt"
        generate_dummy_image(i, img_path, label_path)

print("✅ Dummy dataset generated successfully\n")


# ==============================================================
# 3. CREATE DATA YAML FILE
# ==============================================================

yaml_content = """
train: dataset/images/train
val: dataset/images/val

nc: 4
names: ["gas_cylinder", "electrical_fire", "industrial_fire", "ppe"]
"""

with open("hazard_data.yaml", "w") as f:
    f.write(yaml_content)

print("✅ hazard_data.yaml created\n")


# ==============================================================
# 4. TRAIN YOLOv8 MODEL
# ==============================================================

print("📌 Training YOLOv8 model... This may take a few minutes.\n")

model = YOLO("yolov8n.pt")

model.train(
    data="hazard_data.yaml",
    epochs=5,       # small training, fast (increase for better results)
    imgsz=640,
    batch=8,
    name="hazard_model",
    save=True
)

print("\n🎉 TRAINING COMPLETE!")
print("📁 Model saved at: runs/train/hazard_model/weights/best.pt\n")


# ==============================================================
# 5. COPY MODEL TO PROJECT ROOT AS hazard_model.pt
# ==============================================================

import shutil

if os.path.exists("runs/train/hazard_model/weights/best.pt"):
    shutil.copy("runs/train/hazard_model/weights/best.pt", "hazard_model.pt")
    print("✅ Final model exported as hazard_model.pt in project root folder")
else:
    print("❌ Training completed, but best.pt not found!")
