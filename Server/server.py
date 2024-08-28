from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
from methods import *

app = Flask(__name__)
CORS(app)

facenet512_model = DeepFace.build_model("Facenet512")

@app.route('/')
def home():
    return 'Vanakam da maapla from binary potatoes!'

@app.route('/extract', methods=['POST'])
def upload_file():
    if 'images' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('images')
    name = request.form.get('name', '')
    username = request.form.get('username', '')
    relation = request.form.get('relation', '')
    responses = []
    response, status = process_and_update_images(files, name, username,relation)
    if(status == 200):
        responses.append(response)
    else:
        return jsonify(response), status

    if all(response['message'] for response in responses if 'message' in response):
        return jsonify(responses), 200
    else:
        return jsonify(responses), 400

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status

@app.route('/detect', methods=['POST'])
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

    history_result, history_status = insert_history(user_id, closest_match)
    message, notif_status = send_notification(user_id, closest_match,"face_recognition")
    if notif_status != 200:
        return jsonify(message), notif_status
    
    if history_status != 200:
        return jsonify(history_result), history_status

    return jsonify(match_result), match_status

    


if __name__ == '__main__':
    app.config['DEBUG'] = False
    app.run(host='0.0.0.0', port=5000)
