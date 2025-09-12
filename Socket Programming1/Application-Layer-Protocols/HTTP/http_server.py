from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get", methods=["GET"])
def get_data():
    return jsonify({
        "message": "GET request received successfully",
        "params": request.args
    }), 200

@app.route("/post", methods=["POST"])
def post_data():
    data = request.json if request.is_json else request.form
    return jsonify({
        "message": "POST request received successfully",
        "data": data
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
