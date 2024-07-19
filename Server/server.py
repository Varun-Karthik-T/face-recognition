from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from db import db as database
import os
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Vanakam da maapla from binary potatoes!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    name = request.form.get('name', '')
    
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filename = secure_filename(file.filename)
    temp_path = os.path.join(temp_dir, filename)
    file.save(temp_path)

    try:
        results = DeepFace.represent(img_path=temp_path, model_name="Facenet512", detector_backend="mtcnn")
        os.remove(temp_path)
        
        highest_confidence = 0
        highest_confidence_json = None
        
        for result in results:
            if result['face_confidence'] > highest_confidence:
                highest_confidence = result['face_confidence']
                highest_confidence_json = result
                
        if highest_confidence > 0.85:
            print(f"File uploaded and analyzed successfully. Name: {name}, confidence: {highest_confidence_json['face_confidence']}")
            return jsonify({'message': 'File uploaded and analyzed successfully', 'name': name, 'embedding': highest_confidence_json["embedding"]}), 200
        else:
            return jsonify({'error': 'No face with sufficient confidence found'}), 400
    except Exception as e:
        os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)