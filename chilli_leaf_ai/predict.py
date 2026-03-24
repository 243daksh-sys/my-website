import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Define constants
IMG_SIZE = (224, 224)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'chilli_model.h5')

# Define class names exactly as your folder names
CLASS_NAMES = [
    'cercospora',
    'healthy',
    'murda_complex',
    'nutritional_deficiency',
    'powdery_mildew'
]

# We will load the model globally so it's only loaded once if imported
_model = None

def get_model():
    """Singleton pattern to load the Keras model once."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run train.py first.")
        print(f"[INFO] Loading model from {MODEL_PATH}...")
        _model = load_model(MODEL_PATH)
    return _model

def predict_image(image_path):
    """
    Given an image path, return the predicted class and confidence.
    """
    model = get_model()

    # 1. Load image and resize to 224x224
    img = load_img(image_path, target_size=IMG_SIZE)
    
    # 2. Convert image to array and preprocess for MobileNetV2
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)

    # 3. Expand dimensions to match model input shape (batch_size, 224, 224, 3)
    img_input = np.expand_dims(img_array, axis=0)

    # 4. Predict
    predictions = model.predict(img_input, verbose=0)
    
    # 5. Interpret results
    confidence_scores = predictions[0]
    predicted_class_idx = np.argmax(confidence_scores)
    
    predicted_class = CLASS_NAMES[predicted_class_idx]
    confidence = float(confidence_scores[predicted_class_idx]) * 100.0

    return predicted_class, round(confidence, 2), confidence_scores

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_image>")
        print("Example: python predict.py data/test/sample_leaf.jpg")
        sys.exit(1)

    test_image_path = sys.argv[1]
    
    if not os.path.exists(test_image_path):
        print(f"[ERROR] Image file not found: {test_image_path}")
        sys.exit(1)

    print(f"[INFO] Predicting disease for: {test_image_path}")
    
    try:
        disease_name, conf, all_probs = predict_image(test_image_path)
        
        print("\nClass Probabilities:")
        for i, prob in enumerate(all_probs):
            print(f"{CLASS_NAMES[i]}: {prob*100:.2f}%")
            
        print("\n=========================================")
        print(f"Final Prediction : {disease_name.replace('_', ' ').title()}")
        print(f"Confidence       : {conf}%")
        print("=========================================")
    except Exception as e:
        print(f"[ERROR] {e}")
