# app.py

from flask import Flask
from api.simulate import simulate_bp

def create_app():
    """Create and configure an instance of the Flask application.""" 
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(simulate_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)