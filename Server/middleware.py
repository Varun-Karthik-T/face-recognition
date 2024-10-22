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
    print("Username: " + username)

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    embedding, status = detect_face(file, username)
    if status != 200:
        return jsonify(embedding), status
    print("Embedding extracted")

    match_result, match_status = match_face(username, embedding)
    if match_result.get('success') == True:
        print("Match successful")
    else:
        print("Match failed")
    user_id = match_result.get('user_id')
    closest_match = match_result.get('closest_match')

    file.seek(0)
    image_base64 = base64.b64encode(file.read()).decode('utf-8')

    history_result, history_status = insert_history(user_id, closest_match, image_base64)
    if history_status != 200:
        return jsonify(history_result), history_status
    message, notif_status = send_notification(user_id, closest_match,"face_recognition")
    if notif_status != 200:
        return jsonify(message), notif_status

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
    profiles_collection = database["Profiles"]
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

        # Update the registered_faces in the Users collection
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"registered_faces": updated_faces}}
        )

        # Fetch the user's profiles
        profiles_document = profiles_collection.find_one({"user_id": ObjectId(user_id)})
        if profiles_document:
            profiles = profiles_document.get("profiles", [])
            for profile in profiles:
                profile["allowed_people"] = [pid for pid in profile["allowed_people"] if pid != person_id]

            # Update the profiles in the Profiles collection
            profiles_collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$set": {"profiles": profiles}}
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
    
def send_suspicious_activity_notification(user_id, classification, image):
    try:
        response, status = send_notification(user_id, classification, "suspicious_activity")
        
        if status != 200:
            return jsonify(response), status

        history_response, history_status = insert_history(user_id, classification, image)
        
        if history_status != 200:
            return jsonify(history_response), history_status

        return jsonify({"message": "Notification and history updated successfully"}), 200
    except Exception as e:
        print(f"Error in send_suspicious_activity_notification: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
def add_permission(user_id, entry):
    if not user_id or not entry:
        return jsonify({'error': 'user_id and entry are required', 'success': False}), 400

    permissions_collection = database["Permission"]

    try:
        permission_document = permissions_collection.find_one({"user_id": ObjectId(user_id)})
        print(permission_document)
        if permission_document:
            result = permissions_collection.update_one(
                {"user_id": ObjectId(user_id)},
                {"$push": {"entries": entry}}
            )
            print("Update result:", result.raw_result) 
            if result.modified_count > 0:
                return jsonify({'message': 'Entry added to existing permission document', 'success': True}), 200
            else:
                return jsonify({'error': 'Failed to add entry', 'success': False}), 500
        else:
            new_document = {
                "user_id": user_id,
                "entries": [entry]
            }
            permissions_collection.insert_one(new_document)
            return jsonify({'message': 'Permission document created and entry added', 'success': True}), 200

    except Exception as e:
        print(f"Error in add_permission: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500
    
def get_permissions(user_id):
    if not user_id:
        return jsonify({'error': 'user_id is required', 'success': False}), 400

    permissions_collection = database["Permission"]

    try:
        permission_document = permissions_collection.find_one({"user_id": ObjectId(user_id)})
        if permission_document:
            return jsonify({'entries': permission_document.get('entries', []), 'success': True}), 200
        else:
            return jsonify({'error': 'No permission document found for the user', 'success': False}), 404

    except Exception as e:
        print(f"Error in get_permissions: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500
    
def update_permission(user_id, index, allow):
    if not user_id or index is None or allow is None:
        return jsonify({'error': 'user_id, index, and allow are required', 'success': False}), 400

    permissions_collection = database["Permission"]
    try:
        permission_document = permissions_collection.find_one({"user_id": ObjectId(user_id)})
        if not permission_document:
            return jsonify({'error': 'No permission document found for the user', 'success': False}), 404

        entries = permission_document.get('entries', [])
        if index < 0 or index >= len(entries):
            return jsonify({'error': 'Index out of range', 'success': False}), 400

        entry = entries.pop(index)
        name = entry['name']
        image = entry.get('image', None)
        if allow:
            history_name = name
        else:
            history_name = f"{name} - declined"

        history_response, history_status = insert_history(user_id, history_name, image)
        if history_status != 200:
            return jsonify(history_response), history_status

        permissions_collection.update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": {"entries": entries}}
        )

        return jsonify({'message': 'Permission updated successfully', 'success': True}), 200
    except Exception as e:
        print(f"Error in update_permission: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500