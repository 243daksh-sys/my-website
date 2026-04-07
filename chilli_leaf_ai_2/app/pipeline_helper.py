import os
import sys
import cv2
import uuid
import numpy as np
from ultralytics import YOLO

# Add parent directory to path to import predict.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict import predict_image

# ================= Configuration =================
YOLO_MODEL_PATH = r'E:\Projects\runs\detect\chilli_leaf_yolo4\weights\best.pt'
COLOR_HEALTHY = (0, 255, 0)
COLOR_DISEASE = (0, 0, 255)
# =================================================

print(f"[INFO] Loading YOLO model from {YOLO_MODEL_PATH}...")
try:
    yolo_model = YOLO(YOLO_MODEL_PATH)
except Exception as e:
    print(f"[ERROR] Failed to load YOLO Model: {e}")
    yolo_model = None

def process_image_pipeline(input_path, upload_dir):
    """
    Runs YOLO to find leaves, crops them, classifies each, draws boxes, and returns results.
    """
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Could not read image at {input_path}")
        
    extracted_boxes = []
    
    if yolo_model:
        results = yolo_model(image, conf=0.20, iou=0.60)
        boxes = results[0].boxes
        if len(boxes) > 0:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                extracted_boxes.append((x1, y1, x2, y2))
                
    # OpenCV fallback if YOLO not loaded or finds 0 leaves
    if len(extracted_boxes) == 0:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([95, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x_min, y_min, w, h = cv2.boundingRect(cnt)
            if w > 100 and h > 100:
                extracted_boxes.append((x_min, y_min, x_min + w, y_min + h))

    leaves_data = []
    summary_counts = {}
    
    for bbox in extracted_boxes:
        x1, y1, x2, y2 = bbox
        
        leaf_crop = image[y1:y2, x1:x2]
        if leaf_crop.size == 0:
            continue
            
        crop_id = uuid.uuid4().hex[:8]
        crop_filename = f"crop_{crop_id}.jpg"
        crop_path = os.path.join(upload_dir, crop_filename)
        cv2.imwrite(crop_path, leaf_crop)
        
        try:
            predicted_class, confidence, _ = predict_image(crop_path)
            disease_name_formatted = predicted_class.replace('_', ' ').title()
            
            leaves_data.append({
                'crop_url': f"/static/uploads/{crop_filename}",
                'disease': disease_name_formatted,
                'confidence': float(confidence),
                'bbox': [x1, y1, x2, y2]
            })
            
            summary_counts[disease_name_formatted] = summary_counts.get(disease_name_formatted, 0) + 1
            
            box_color = COLOR_HEALTHY if predicted_class.lower() == 'healthy' else COLOR_DISEASE
            label = f"{disease_name_formatted} ({confidence}%)"
            
            cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
            (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image, (x1, y1 - text_height - baseline - 10), (x1 + text_width, y1), box_color, -1)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        except Exception as e:
            print(f"[WARNING] Failed to analyze crop {crop_path}: {e}")
            
    base_name = os.path.basename(input_path)
    annotated_filename = f"annotated_{uuid.uuid4().hex[:4]}_{base_name}"
    annotated_path = os.path.join(upload_dir, annotated_filename)
    cv2.imwrite(annotated_path, image)
    
    return {
        'annotated_image_url': f"/static/uploads/{annotated_filename}",
        'leaves': leaves_data,
        'total_leaves': len(leaves_data),
        'summary_counts': summary_counts
    }
