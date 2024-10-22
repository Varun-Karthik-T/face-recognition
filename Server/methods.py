from deepface import DeepFace
from werkzeug.utils import secure_filename
from db import db as database
import os
import re
import numpy as np
from pymongo import ReturnDocument
from datetime import datetime
from bson import ObjectId
from scipy.spatial import distance
from models import profiles_schema

THRESHOLD = 0.3

def process_and_update_images(files, name, username, relation):
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    embeddings = []
    errors = []

    for file in files:
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
                embeddings.append(highest_confidence_json["embedding"])
            else:
                errors.append(f"No face with sufficient confidence found in file {filename}")
        except Exception as e:
            os.remove(temp_path)
            errors.append(f"Error in processing file: {filename}")
            continue
    if errors:
        print(errors)
        return {"success": False,"error" : errors}, 500
    if embeddings:
        collection = database["Users"]
        user_record = collection.find_one({"name": username})
        if not user_record:
            print("User not found")
            return {"success":False,'error': ['User not found']}, 404

        new_id = max([face.get('id', 0) for face in user_record.get('registered_faces', [])], default=0) + 1

        face_data = {
            "id": new_id,
            "name": name,
            "relation": relation,
            "embeddings": embeddings
        }

        try:
            document = collection.find_one_and_update(
                {"name": username},
                {"$push": {"registered_faces": face_data}},
                return_document=ReturnDocument.AFTER
            )
            if document:
                return {"success":True,'message': f'{name} has been registered!'}, 200
            else:
                print("Failed to update user record")
                return {"success":False,'error': ['User not found']}, 404
        except Exception as e:
            print(f"Error in updating user record: {str(e)}")
            return {"success":False,'error': [str(e)]}, 500
    else:
        print("No valid embeddings found")
        return {"success":False,'error': ['No valid embeddings found']}, 400

def register_user(data):
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    if not name.strip() or not phone.strip() or not email.strip():
        return {'error': 'Name and phone are required', 'success': False}, 400
    
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return {'error': 'Invalid email format', 'success': False}, 400

    phone_regex = r'^\d{10}$'
    if not re.match(phone_regex, phone):
        return {'error': 'Invalid phone format', 'success': False}, 400

    user_document = {
        "name": name,
        "phone": phone,
        "email": email,
        "registered_faces": []
    }

    try:
        collection = database["Users"]
        existing_user = collection.find_one({"email": email})
        if existing_user:
            return {'error': 'User with this email already exists', 'success': False}, 400

        result = collection.insert_one(user_document)
        user_id = result.inserted_id

        history_document = {
            "user_id": user_id,
            "history": []
        }
        history_collection = database["History"]
        history_collection.insert_one(history_document)
        
        profiles = [{"id":i,"profile_name":f"profile_{i}","allowed_people":[]} for i in range(5)]
        
        profile_document = {
            "user_id": user_id,
            "profiles": profiles
        }
        
        profile_collection = database["Profiles"]
        profile_collection.insert_one(profile_document)
        
        notification_document = {
            "user_id" : user_id,
            "suspicious_activity" : [], 
            "face_recognition" : []
        }
        
        notification_collection = database["Notifications"]
        notification_collection.insert_one(notification_document)
        
        return {'message': 'User registered successfully', 'success': True}, 200
    except Exception as e:
        return {'error': str(e), 'success': False}, 500
    
def detect_face(file, username):
    try:
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        filename = secure_filename(file.filename)
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        embedding = DeepFace.represent(img_path=temp_path, model_name="Facenet512", detector_backend="mtcnn")
        os.remove(temp_path)
        return embedding[0]["embedding"], 200
    except Exception as e:
        print(f"Error in detecting face: {str(e)}")
        return {'error': str(e), "success" : False}, 500
    
def match_face(username, embedding):
    users_collection = database['Users']
    
    try:
        user_record = users_collection.find_one({"name": username})
        if not user_record:
            return {'error': 'User not found'}, 404
        registered_faces = user_record.get('registered_faces', [])
        closest_match = None
        cosine_distance = None
        for face in registered_faces:
            name = face['name']
            embeddings = face['embeddings']
            for db_embedding in embeddings:
                cosine_dist = distance.cosine(embedding, db_embedding)
                if cosine_dist <= THRESHOLD:
                    closest_match = name
                    break
        if closest_match is None:
                return {
                    'user_id': str(user_record['_id']),
                    'username': username,
                    'closest_match': "Unknown person",
                    'cosine_distance': cosine_distance,
                    "success" : False
                    }, 200
        return {
            'user_id': str(user_record['_id']),
            'username': username,
            'closest_match': closest_match,
            'cosine_distance': cosine_distance,
            "success" : True
        }, 200    
    except Exception as e:
        print(f"Error in matching face: {str(e)}")
        return {'error': str(e), "success" : False}, 500
    
def insert_history(user_id, name, image):
    print("Inserting history")
    print(user_id)
    try:
        collection = database["History"]
        print(collection)
        today = datetime.utcnow().date()

        user_history = collection.find_one({"user_id": ObjectId(user_id)})

        if not user_history:
            return {'error': 'User history not found', "success" : False}, 404

        history_entry = next((entry for entry in user_history['history'] if entry['date'].date() == today), None)
        
        new_id = max([entry['id'] for history in user_history['history'] for entry in history['entries']], default=0) + 1

        new_entry = {
            "id": new_id,
            "name": name,
            "timestamp": datetime.utcnow(),
            "image": image
        }

        if history_entry:
            history_entry['entries'].append(new_entry)
        else:
            new_history_entry = {
                "date": datetime.utcnow(),
                "entries": [new_entry]
            }
            user_history['history'].append(new_history_entry)

        updated_history = collection.find_one_and_update(
            {"user_id": ObjectId(user_id)},
            {"$set": {"history": user_history['history']}},
            return_document=ReturnDocument.AFTER
        )

        if updated_history:
            return {'message': 'History updated successfully', "success" : True}, 200
        else:
            return {'error': 'Failed to update history', "success" : False}, 500
    except Exception as e:
        print(f"Error in insert_history: {str(e)}")
        return {'error': str(e), "success" : False}, 500
    
def send_notification(user_id, content, type):
    print("Sending notification")
    collection = database["Notifications"]
    if type == "face_recognition":
        notification_entry = {
            "timestamp": datetime.utcnow(),
            "name": content
        }
        print(notification_entry)
    else:
        notification_entry = {
            "timestamp": datetime.utcnow(),
            "classification": content
        }

    try:
        updated_notification = collection.find_one_and_update(
            {"user_id": ObjectId(user_id)},
            {"$push": {"suspicious_activity" if type == "suspicious_activity" else "face_recognition": notification_entry}},
            return_document=ReturnDocument.AFTER
        )
        print(updated_notification)

        if updated_notification:
            return {'message': 'Notification sent successfully', "success" : True}, 200
        else:
            return {'error': 'Failed to send notification', "success" : False}, 500
    except Exception as e:
        return {'error': str(e)}, 500
