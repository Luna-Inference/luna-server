# Central server for status, routing & detection
from flask import Flask, jsonify
from flask_cors import CORS
from config import *
app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

@app.route('/luna', methods=['GET'])
def luna_recognition():
    """Device recognition endpoint"""
    return jsonify({"device": "luna"})

if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)