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

if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=5000)
