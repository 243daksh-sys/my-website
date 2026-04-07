from ultralytics import YOLO

def main():
    # 1. Load the pre-trained YOLO11 Nano model
    # The '.pt' file will automatically download the first time you run this.
    model = YOLO("yolo11n.pt") 

    # 2. Set the path to your dataset's YAML file
    # This automatically uses the data.yaml created by the convert_dataset.py script!
    data_yaml_path = "datasets/data.yaml"
    
    print(f"Starting training on {data_yaml_path}...")
    
    # 3. Train the model
    results = model.train(
        data=data_yaml_path,
        epochs=50,       # Train for 50 cycles over your entire dataset
        imgsz=640,       # Resize images to 640x640 pixels during training
        batch=16,        # Process 16 images at a time (lower to 8 or 4 if you run out of memory)
        # device='cpu',  # Uncomment this line if your script crashes because you don't have an NVIDIA GPU
        name="chilli_leaf_yolo" # Folder name where the results will be saved
    )

    print("\n[INFO] Training Complete!")
    print("[INFO] Your trained model is saved at: runs/detect/chilli_leaf_yolo/weights/best.pt")

if __name__ == '__main__':
    main()
