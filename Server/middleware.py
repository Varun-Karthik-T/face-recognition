from flask import request, jsonify
from db import db as database 
from bson import ObjectId
from pymongo import ReturnDocument
from methods import *
import base64


def home():
    return 'Vanakam da maapla from binary potatoes!'

def upload_file():
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('images')
    name = request.form.get('name', '')
    username = request.form.get('username', '')
    relation = request.form.get('relation', '')
    response, status = process_and_update_images(files, name, username,relation)
    return jsonify(response), status
    
def register():
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status

def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    username = request.form.get('username', '')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    embedding, status = detect_face(file, username)
    if status != 200:
        return jsonify(embedding), status
    print("Embedding extracted")

    match_result, match_status = match_face(username, embedding)
    if match_status != 200:
        print("Match failed")
        return jsonify(match_result), match_status
    print("Match successful")
    user_id = match_result.get('user_id')
    closest_match = match_result.get('closest_match')

    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')
    print("Image base64 encoded: " + image_base64)

    history_result, history_status = insert_history(user_id, closest_match, image_base64)
    message, notif_status = send_notification(user_id, closest_match,"face_recognition")
    if notif_status != 200:
        return jsonify(message), notif_status
    
    if history_status != 200:
        return jsonify(history_result), history_status

    return jsonify(match_result), match_status

def get_profiles(user_id):
    profiles_collection = database["Profiles"]
    users_collection = database["Users"]
    profiles_document = profiles_collection.find_one({"user_id": ObjectId(user_id)}, {"_id": 0})
    if not profiles_document:
        return jsonify({"error": "Profiles not found"}), 404
    user_record = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "registered_faces": 1})
    if not user_record:
        return jsonify({"error": "User not found"}), 404

    registered_faces = user_record.get("registered_faces", [])
    registered_faces_dict = {}
    for face in registered_faces:
        face_id = face["id"]
        if "embeddings" in face:
            del face["embeddings"]
        registered_faces_dict[face_id] = face
    for profile in profiles_document["profiles"]:
        profile["allowed_people"] = [registered_faces_dict.get(person_id, {"id": person_id, "name": "Unknown"}) for person_id in profile["allowed_people"]]

    profiles_document['user_id'] = str(profiles_document['user_id'])
    return jsonify(profiles_document), 200

def update_profile(user_id, profile_id):
    profiles_collection = database["Profiles"]
    profile_data = request.json
    print(" Profile ID: " + profile_id)

    if 'allowed_people' in profile_data:
        profile_data['allowed_people'] = [person['id'] for person in profile_data['allowed_people']]
    
    profiles_document = profiles_collection.find_one({"user_id": ObjectId(user_id)})
    if not profiles_document:
        return jsonify({"error": "Profiles not found"}), 404
    print("Profiles found" + str(profiles_document))

    profile_index = next((index for (index, d) in enumerate(profiles_document['profiles']) if d.get('id') == int(profile_id)), None)
    if profile_index is None:
        return jsonify({"error": "Profile not found"}), 404

    profiles_document['profiles'][profile_index].update(profile_data)

    updated_document = profiles_collection.find_one_and_update(
        {"user_id": ObjectId(user_id)},
        {"$set": {"profiles": profiles_document['profiles']}},
        return_document=ReturnDocument.AFTER
    )

    if updated_document:
        return jsonify({"message": "Profile updated successfully", "profiles": updated_document['profiles']}), 200
    else:
        return jsonify({"error": "Failed to update profile"}), 500
    
def get_registered_faces(user_id):
    users_collection = database["Users"]
    try:
        user_record = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "registered_faces": 1})
        if not user_record:
            print("User not found")
            return jsonify({"error": "User not found"}), 404
        registered_faces = user_record.get("registered_faces", [])
        for face in registered_faces:
            if 'embeddings' in face:
                del face['embeddings']
        return jsonify(user_record["registered_faces"]), 200
    except Exception as e:
        print(f"Error in get_registered_faces: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def delete_registered_face(user_id, person_id):
    users_collection = database["Users"]
    person_id = int(person_id)
    try:
        user_record = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_record:
            print("User not found")
            return jsonify({"error": "User not found"}), 404

        registered_faces = user_record.get("registered_faces", [])
        updated_faces = [face for face in registered_faces if face.get("id") != person_id]

        if len(registered_faces) == len(updated_faces):
            print("Person not found")
            return jsonify({"error": "Person not found"}), 404

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"registered_faces": updated_faces}}
        )

        return jsonify({"message": "Person deleted successfully"}), 200
    except Exception as e:
        print(f"Error in delete_registered_face: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_history(user_id):
    collection = database["History"]
    try:
        user_history = collection.find_one({"user_id": ObjectId(user_id)}, {"_id": 0, "history": 1})
        if not user_history:
            return jsonify({"error": "User history not found"}), 404
        return jsonify(user_history["history"]), 200
    except Exception as e:
        print(f"Error in get_history: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def get_notifications(user_id):
    collection = database["Notifications"]
    try:
        user_notifications = collection.find_one({"user_id": ObjectId(user_id)}, {"_id": 0, "suspicious_activity": 1, "face_recognition": 1})
        if not user_notifications:
            return jsonify({"error": "User notifications not found"}), 404
        return jsonify(user_notifications), 200
    except Exception as e:
        print(f"Error in get_notifications: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def set_active_profile(user_id, profile_id):
    users_collection = database["Users"]
    try:
        user_record = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user_record:
            return jsonify({"error": "User not found"}), 404

        profiles_collection = database["Profiles"]
        profile_record = profiles_collection.find_one({"user_id": ObjectId(user_id), "profiles.id": int(profile_id)})
        if not profile_record:
            return jsonify({"error": "Profile not found"}), 404

        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"active_profile_id": int(profile_id)}}
        )

        return jsonify({"message": "Active profile set successfully"}), 200
    except Exception as e:
        print(f"Error in set_active_profile: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_active_profile(user_id):
    users_collection = database["Users"]
    try:
        user_record = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "active_profile_id": 1})
        if not user_record:
            return jsonify({"error": "User not found"}), 404

        active_profile_id = user_record.get("active_profile_id")
        if active_profile_id is None:
            return jsonify({"error": "Active profile not set"}), 404

        return jsonify({"active_profile_id": active_profile_id}), 200
    except Exception as e:
        print(f"Error in get_active_profile: {str(e)}")
        return jsonify({"error": str(e)}), 500