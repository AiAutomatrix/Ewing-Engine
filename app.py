# app.py

from flask import Flask
from api.simulate import simulate_bp
from api.root import root_bp
from api.health import health_bp
from api.capabilities import capabilities_bp

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(simulate_bp, url_prefix="/simulate")
    app.register_blueprint(root_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(capabilities_bp)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)