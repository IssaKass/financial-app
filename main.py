from flask import Flask, jsonify
import os
import random

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"number": random.random()})


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
