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
    
    responses = []
    for file in files:
        response, status = process_and_update_image(file, name, username)
        if(status == 200):
            responses.append(response)
        else:
            return jsonify(response), status

    if all(response['message'] for response in responses if 'message' in response):
        return jsonify(responses), 200
    else:
        return jsonify(responses), 400
    


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=5000)
