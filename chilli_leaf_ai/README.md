# Chilli Leaf Disease Classification System

This is a complete end-to-end AI system to classify chilli leaf images into 5 categories using MobileNetV2.

## Categories:
1. Cercospora
2. Healthy
3. Murda Complex
4. Nutritional Deficiency
5. Powdery Mildew

## System Features
- **Auto-Environment Setup** (`setup.bat` for Windows, `setup.sh` for Mac/Linux)
- **Transfer Learning Training** via `train.py`
- **Standalone Prediction** via `predict.py`
- **Web Application** via Flask in `app/app.py`

## Quick Start
### 1. Setup & Install Dependencies
**Windows:**
Double click `setup.bat` or run it entirely in your terminal. It will install Python (if missing), configure a virtual environment, and install dependencies automatically.
**Mac/Linux:**
Run `bash setup.sh`

### 2. Populate Data
Place your image datasets inside the `data/train/` folder properly segregated into subfolders:
- `data/train/cercospora/`
- `data/train/healthy/`
... and so on.

### 3. Train the Model
Make sure your virtual environment is active:
```bash
venv\Scripts\activate   # Windows
# or
source venv/bin/activate # Mac/Linux
```
Then run:
```bash
python train.py
```
This will train the model leveraging MobileNetV2 and save it as `models/chilli_model.h5`.

### 4. Direct Prediction (CLI)
You can directly classify an image from the terminal:
```bash
python predict.py data/test/sample_leaf.jpg
```

### 5. Web App Usage
Start the Flask web app for the UI component:
```bash
cd app
python app.py
```
After it launches, open your browser and navigate to: http://127.0.0.1:5000/
Upload your chilli leaf images via the Web UI to get predictions instantly!
