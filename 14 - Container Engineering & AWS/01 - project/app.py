from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "dockerized-data-api"
    })


@app.post("/process")
def process():
    data = request.get_json(silent=True) or {}

    return jsonify({
        "message": "Data processed successfully",
        "received": data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)