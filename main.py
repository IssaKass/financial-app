"""Main script to run the Flask application."""

import os
from flask import Flask, jsonify
from api import create_app

if __name__ == "__main__":
    APP = create_app("development")

    APP = Flask(__name__)

    APP.route("/")

    def test():
        return jsonify(
            {
                "random": "56",
                "random float": "87.247",
                "bool": "false",
                "date": "1989-07-08",
                "regEx": "helloo to you",
                "enum": "online",
                "firstname": "Rani",
                "lastname": "Kat",
                "city": "Saint-Denis",
                "country": "Panama",
                "countryCode": "SY",
                "email uses current data": "Rani.Kat@gmail.com",
                "email from expression": "Rani.Kat@yopmail.com",
                "array": ["Madelle", "Amara", "Mallory", "Quintina", "Oona"],
                "array of objects": [
                    {"index": "0", "index start at 5": "5"},
                    {"index": "1", "index start at 5": "6"},
                    {"index": "2", "index start at 5": "7"},
                ],
                "Catrina": {"age": "49"},
            }
        )

    APP.run(debug=True, port=os.getenv("PORT", default=5000))
