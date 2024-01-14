"""Main script to run the Flask application."""

import os
from api import create_app

if __name__ == "__main__":
    APP = create_app("development")

    APP.run(debug=True, port=os.getenv("PORT", default=5000))
