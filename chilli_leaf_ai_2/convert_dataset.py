import os
import csv
import ast

def convert_to_yolo():
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(base_dir, 'datasets')
    csv_path = os.path.join(dataset_dir, 'train.csv')
    train_dir = os.path.join(dataset_dir, 'train')
    
    if not os.path.exists(csv_path):
        print(f"[ERROR] Could not find {csv_path}")
        return

    print("[INFO] Converting train.csv to YOLO format...")
    
    # Clear existing .txt files in train directory to prevent duplicate boxes
    # if the script happens to be run multiple times.
    for file in os.listdir(train_dir):
        if file.endswith('.txt'):
            os.remove(os.path.join(train_dir, file))
            
    converted_count = 0
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_id = row['image_id']
            img_w = float(row['width'])
            img_h = float(row['height'])
            
            # The bbox is a string like "[473, 273, 289, 335]" (x_min, y_min, width, height)
            bbox = ast.literal_eval(row['bbox'])
            x_min, y_min, box_w, box_h = map(float, bbox)
            
            # Calculate YOLO format (normalized center_x, center_y, width, height)
            x_center = (x_min + (box_w / 2.0)) / img_w
            y_center = (y_min + (box_h / 2.0)) / img_h
            w_norm = box_w / img_w
            h_norm = box_h / img_h
            
            # Ensure values are strictly bounded between 0 and 1
            x_center = max(0.0, min(1.0, x_center))
            y_center = max(0.0, min(1.0, y_center))
            w_norm = max(0.0, min(1.0, w_norm))
            h_norm = max(0.0, min(1.0, h_norm))
            
            # Create the .txt filename
            txt_filename = os.path.splitext(image_id)[0] + '.txt'
            txt_path = os.path.join(train_dir, txt_filename)
            
            # Write to the file in append mode (since one image has multiple leaves/rows)
            with open(txt_path, 'a') as txt_file:
                # class_id is 0 because there is only one class: 'leaf'
                txt_file.write(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
                
            converted_count += 1
            
    print(f"[SUCCESS] Converted {converted_count} bounding boxes into YOLO format!")

    # Create the data.yaml file needed for Ultralytics YOLO
    yaml_path = os.path.join(dataset_dir, 'data.yaml')
    with open(yaml_path, 'w') as yf:
        yf.write(f"train: {os.path.abspath(train_dir)}\n")
        # We use train as val for simplicity, but YOLO will split it automatically or just track training metrics
        yf.write(f"val: {os.path.abspath(train_dir)}\n")  
        yf.write(f"nc: 1\n")
        yf.write(f"names: ['leaf']\n")
        
    print(f"[SUCCESS] Created YOLO configuration file at: {yaml_path}")
    print("\n>>> You are now completely ready to train! Just run: python train_yolo.py")

if __name__ == '__main__':
    convert_to_yolo()
