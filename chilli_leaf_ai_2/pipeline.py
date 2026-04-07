import os
import cv2
import shutil
import numpy as np
from ultralytics import YOLO, YOLOWorld
from predict import predict_image

# ================= Configuration =================
INPUT_IMAGE_PATH = 'test.jpg'  # Replace with your input image
OUTPUT_IMAGE_PATH = 'labeled_output.jpg'
TEMP_CROP_DIR = 'temp_leaves'
YOLO_MODEL_PATH = r'E:\Projects\runs\detect\chilli_leaf_yolo4\weights\best.pt'  # Custom trained model
# =================================================

# Colors in BGR format for OpenCV
COLOR_HEALTHY = (0, 255, 0)  # Green
COLOR_DISEASE = (0, 0, 255)  # Red


def main():
    print(f"[INFO] Initializing multi-stage plant pathology pipeline...")

    # ---------------------------------------------------------
    # Detection Stage
    # ---------------------------------------------------------
    print(f"[STAGE 1] Loading YOLO model from {YOLO_MODEL_PATH}...")
    try:
        if 'world' in YOLO_MODEL_PATH.lower():
            # YOLOWorld supports open-vocabulary detection without custom training
            yolo_model = YOLOWorld(YOLO_MODEL_PATH)
            yolo_model.set_classes(["leaf", "plant leaf"])
        else:
            yolo_model = YOLO(YOLO_MODEL_PATH)
    except Exception as e:
        print(f"[ERROR] Failed to load YOLO model: {e}")
        return

    # Clean / prepare temporary directory for crops
    if os.path.exists(TEMP_CROP_DIR):
        shutil.rmtree(TEMP_CROP_DIR)
    os.makedirs(TEMP_CROP_DIR, exist_ok=True)

    print(f"[INFO] Reading image: {INPUT_IMAGE_PATH}")
    image = cv2.imread(INPUT_IMAGE_PATH)
    if image is None:
        print(f"[ERROR] Could not read image at '{INPUT_IMAGE_PATH}'. Please check the path.")
        return

    print("[STAGE 1] Running leaf detection...")
    # Using conf=0.20 and iou=0.60 to detect multiple overlapping dense leaves
    results = yolo_model(image, conf=0.20, iou=0.60)

    # YOLO results is a list per image; we only passed one image
    result = results[0]
    boxes = result.boxes

    print(f"[INFO] YOLO detected {len(boxes)} potential leaves.")

    # ---------------------------------------------------------
    # OpenCV Fallback (If YOLO finds 0 leaves)
    # ---------------------------------------------------------
    extracted_boxes = []
    if len(boxes) == 0:
        print("[WARNING] Zero-shot YOLO failed to segment the dense leaves.")
        print("[INFO] Falling back to OpenCV Color & Contour Detection...")
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range of green color in HSV spaces
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([95, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            x_min, y_min, w, h = cv2.boundingRect(cnt)
            # Filter for reasonably sized leaves (avoid tiny noise spots)
            if w > 100 and h > 100:
                extracted_boxes.append((x_min, y_min, x_min + w, y_min + h))
                
        print(f"[INFO] OpenCV fallback detected {len(extracted_boxes)} potential leaves.")
    else:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            extracted_boxes.append((x1, y1, x2, y2))

    health_counts = {}
    total_analyzed = 0

    # Process each detected bounding box
    for i, bbox in enumerate(extracted_boxes):
        # Extract bounding box coordinates
        x1, y1, x2, y2 = bbox

        # ---------------------------------------------------------
        # Extraction Stage
        # ---------------------------------------------------------
        # Crop the leaf image
        leaf_crop = image[y1:y2, x1:x2]

        if leaf_crop.size == 0:
            continue

        temp_path = os.path.join(TEMP_CROP_DIR, f"leaf_{i}.jpg")
        cv2.imwrite(temp_path, leaf_crop)

        # ---------------------------------------------------------
        # Analysis Stage
        # ---------------------------------------------------------
        # Pass through the existing Chilli Leaf Classifier
        try:
            predicted_class, confidence, _ = predict_image(temp_path)

            # ---------------------------------------------------------
            # Aggregation Stage
            # ---------------------------------------------------------
            total_analyzed += 1
            if predicted_class not in health_counts:
                health_counts[predicted_class] = 0
            health_counts[predicted_class] += 1

            # ---------------------------------------------------------
            # Visualization Stage
            # ---------------------------------------------------------
            disease_name_formatted = predicted_class.replace('_', ' ').title()
            label = f"{disease_name_formatted} ({confidence}%)"

            if predicted_class.lower() == 'healthy':
                box_color = COLOR_HEALTHY
            else:
                box_color = COLOR_DISEASE

            # Draw the bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)

            # Draw an opaque background for the text
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image, (x1, y1 - text_height - baseline - 10),
                          (x1 + text_width, y1), box_color, -1)

            # Overlay the text label
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        except Exception as e:
            print(f"[WARNING] Failed to analyze crop {temp_path}: {e}")

    # Save final visualized image
    cv2.imwrite(OUTPUT_IMAGE_PATH, image)
    print(f"\n[STAGE 5] Visualization saved to: {OUTPUT_IMAGE_PATH}")

    # ---------------------------------------------------------
    # Final Summary (Aggregation)
    # ---------------------------------------------------------
    print("\n=========================================")
    print("      PLANT PATHOLOGY PIPELINE SUMMARY    ")
    print("=========================================")
    print(f"Total Leaves Analyzed : {total_analyzed}")

    healthy_count = health_counts.get('healthy', 0)
    print(f"Healthy Leaves        : {healthy_count}")

    print("\nDiseases Found:")
    diseases_found = False
    for disease, count in health_counts.items():
        if disease != 'healthy':
            disease_title = disease.replace('_', ' ').title()
            print(f" - {count} {disease_title}")
            diseases_found = True

    if not diseases_found:
        print(" - None")
    print("=========================================")


if __name__ == '__main__':
    main()
