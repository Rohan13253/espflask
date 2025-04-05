from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

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
        sensor_id = data.get('sensor_id')

        if not sensor_id:
            return jsonify({"status": "fail", "reason": "Missing sensor_id"}), 400

        # Map sensor ID to node name
        node_map = {
            "A": "node1",
            "B": "node2",
            "C": "node3"
        }

        node = node_map.get(sensor_id.upper(), "node4")  # fallback to node4 if unknown

        # Save the data to the corresponding node
        ref = db.reference(f"/sensors/{node}")
        ref.set({
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "gas": data.get("gas"),
            "sensor_id": sensor_id
        })

        return jsonify({"status": "success", "message": f"Data saved under {node}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to 10000 if PORT not set
    app.run(host='0.0.0.0', port=port)
