from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Required for frontend communication

# Load environment variables
load_dotenv()

# Initialize Flask app with CORS support
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase
cred = credentials.Certificate("/etc/secrets/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://flare-cade7-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route("/")
def home():
    """Health check endpoint"""
    return "Flask API is working!"

@app.route("/upload", methods=["POST"])
def upload_data():
    """
    Endpoint for uploading sensor data to Firebase
    Expected JSON payload:
    {
        "sensor_id": "A"/"B"/"C",
        "temperature": number,
        "humidity": number,
        "gas": number
    }
    """
    data = request.json
    if not data:
        return jsonify({"status": "fail", "reason": "No data received"}), 400

    try:
        sensor_id = data.get('sensor_id')
        if not sensor_id:
            return jsonify({"status": "fail", "reason": "Missing sensor_id"}), 400

        # Map physical sensor ID to Firebase node
        node_map = {
            "A": "node1",
            "B": "node2",
            "C": "node3"
        }
        node = node_map.get(sensor_id.upper(), "node4")  # Default to node4 if unknown

        # Save data to Firebase
        ref = db.reference(f"/sensors/{node}")
        ref.set({
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "gas": data.get("gas"),
            "sensor_id": sensor_id
        })

        return jsonify({
            "status": "success",
            "message": f"Data saved under {node}",
            "node": node,
            "received_data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "received_data": data
        }), 500

@app.route("/sensors", methods=["GET"])
def get_all_sensors():
    """
    Endpoint for retrieving all sensor data from Firebase
    Returns:
    {
        "node1": {sensor_data},
        "node2": {sensor_data},
        ...
    }
    """
    try:
        ref = db.reference("/sensors")
        sensors = ref.get()
        
        # Return empty object if no data exists
        return jsonify(sensors if sensors else {})
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
