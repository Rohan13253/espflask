from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()  # 👈 Load the .env file

app = Flask(__name__)

cred = credentials.Certificate("/etc/secrets/firebase_key.json")  # or .json if renamed
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://flare-cade7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route("/")
def home():
    return "Flask API is working!"

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.json
    if not data:
        return jsonify({"status": "fail", "reason": "No data received"}), 400

    try:
        # Push to Firebase Realtime Database under a new key
        ref = db.reference("/sensor_data")
        ref.push(data)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to 10000 if PORT not set
    app.run(host='0.0.0.0', port=port)

