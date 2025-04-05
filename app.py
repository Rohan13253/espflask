from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "ESP32 Flask API is running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    print("Data received:", data)
    return jsonify({"status": "success", "message": "Data received!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
