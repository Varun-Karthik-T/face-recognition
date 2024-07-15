from flask import Flask
from flask_cors import CORS
from db import db as database

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Vanakam da maapla from binary potatoes!'

if __name__ == '__main__':
    app.run(debug=True)