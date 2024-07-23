from deepface import DeepFace
from werkzeug.utils import secure_filename
from db import db as database
import os
from pymongo import ReturnDocument

username = "Salai"

def process_and_update_image(file, name):
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
            print(f"File analyzed successfully. Name: {name}, confidence: {highest_confidence_json['face_confidence']}")
            collection = database["Users"]
            document = collection.find_one_and_update({"name": username},{"$push": {"registered_faces": {"name": name, "embedding" : highest_confidence_json["embedding"]}}}, return_document=ReturnDocument.AFTER)
            if document:
                return {'message': 'File uploaded and analyzed successfully'}, 200
            else:
                return {'error': 'User not found'}, 404
        else:
            return {'error': 'No face with sufficient confidence found'}, 400
    except Exception as e:
        os.remove(temp_path)
        return {'error': str(e)}, 500
