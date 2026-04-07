import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Import pipeline helper instead of predict.py
from pipeline_helper import process_image_pipeline

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Predict
            result_data = process_image_pipeline(file_path, app.config['UPLOAD_FOLDER'])
            result_data['success'] = True
            
            # Return prediction result
            return jsonify(result_data)
        except Exception as e:
            return jsonify({'error': str(e)})
            
    return jsonify({'error': 'Invalid file format. Please upload a JPG or PNG.'})

if __name__ == '__main__':
    print("[INFO] Starting Flask Server...")
    print("[INFO] Ensure you have run 'python train.py' to generate the model first.")
    app.run(debug=True, port=5000)
