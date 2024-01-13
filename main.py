"""Main script to run the Flask application."""

from api import create_app

if __name__ == "__main__":
    APP = create_app(environment="development")
    APP.run(debug=True, port=5000)
