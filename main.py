# """Main script to run the Flask application."""

import os
from api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
