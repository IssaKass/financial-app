# """Main script to run the Flask application."""

# import os
# from flask import Flask, jsonify
# from api import create_app

# app = Flask(__name__)


# @app.route("/")
# def test():
#     return jsonify(
#         {
#             "random": "56",
#             "random float": "87.247",
#             "bool": "false",
#             "date": "1989-07-08",
#             "regEx": "helloo to you",
#             "enum": "online",
#             "firstname": "Rani",
#             "lastname": "Kat",
#             "city": "Saint-Denis",
#             "country": "Panama",
#             "countryCode": "SY",
#             "email uses current data": "Rani.Kat@gmail.com",
#             "email from expression": "Rani.Kat@yopmail.com",
#             "array": ["Madelle", "Amara", "Mallory", "Quintina", "Oona"],
#             "array of objects": [
#                 {"index": "0", "index start at 5": "5"},
#                 {"index": "1", "index start at 5": "6"},
#                 {"index": "2", "index start at 5": "7"},
#             ],
#             "Catrina": {"age": "49"},
#         }
#     )


# if __name__ == "__main__":
#     # APP = create_app("development")

#     app.run(debug=True, port=os.getenv("PORT", default=5000))

import os
from api import create_app
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=os.getenv("PORT", default=5000))
