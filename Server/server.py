from flask import Flask
from flask_cors import CORS
from middleware import *
from deepface import DeepFace

facenet512_model = DeepFace.build_model("Facenet512")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home_route():
    return home()

@app.route('/people', methods=['POST'])
def upload_file_route():
    return upload_file()

@app.route('/register', methods=['POST'])
def register_route():
    return register()

@app.route('/detect', methods=['POST'])
def detect_route():
    return detect()

@app.route('/profiles/<user_id>', methods=['GET'])
def get_profiles_route(user_id):
    return get_profiles(user_id)

@app.route('/profiles/<user_id>/<profile_id>', methods=['PUT'])
def update_profile_route(user_id, profile_id):
    return update_profile(user_id, profile_id)

@app.route('/people/<user_id>', methods=['GET'])
def get_registered_faces_route(user_id):
    return get_registered_faces(user_id)

@app.route('/people/<user_id>/<person_id>', methods=['DELETE'])
def delete_registered_face_route(user_id, person_id):
    return delete_registered_face(user_id, person_id)

@app.route('/history/<user_id>', methods=['GET'])
def get_history_route(user_id):
    return get_history(user_id)

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications_route(user_id):
    return get_notifications(user_id)

@app.route('/profiles/<user_id>/active', methods=['PUT'])
def set_active_profile_route(user_id):
    profile_id = request.json.get('profile_id')
    return set_active_profile(user_id, profile_id)

@app.route('/profiles/<user_id>/active', methods=['GET'])
def get_active_profile_route(user_id):
    return get_active_profile(user_id)

@app.route('/notifications/<user_id>/suspicious', methods=['POST'])
def send_suspicious_activity_notification_route(user_id):
    classification = request.form.get('classification')
    image = request.files.get('image')
    
    if not classification:
        return jsonify({"error": "Classification is required"}), 400
    if not image:
        return jsonify({"error": "Image is required"}), 400
    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    
    return send_suspicious_activity_notification(user_id, classification, image_base64)

@app.route('/permissions/<user_id>', methods=['POST'])
def add_permission_route(user_id):
    name = request.form.get('name')
    reason = request.form.get('reason')
    image = request.files.get('image')
    
    print("name: ", name)
    print("reason: ", reason)
    

    if not name or not reason or not image:
        return jsonify({'error': 'Name, reason, and image are required'}), 400

    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    entry = {"name": name, "reason": reason, "allow": False, "image": image_base64}
    return add_permission(user_id, entry)

@app.route('/permissions/<user_id>', methods=['GET'])
def get_permissions_route(user_id):
    return get_permissions(user_id)

@app.route('/permissions/<user_id>/<int:index>', methods=['PUT'])
def update_permission_route(user_id, index):
    allow = request.json.get('allow')
    return update_permission(user_id, index, allow)

if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=5000)
