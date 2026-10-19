
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(
        project="Project 14 - Container Engineering & AWS",
        message="My first containerized Python web application is running!",
        status="success"
    )


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
