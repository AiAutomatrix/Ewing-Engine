# api/root.py

from flask import Blueprint, jsonify

root_bp = Blueprint("root_bp", __name__)

@root_bp.route("/")
def root():
    """Root endpoint to confirm the app is alive."""
    return jsonify(
        {
            "service": "Ewing Engine",
            "status": "running",
            "version": "0.11",
            "mode": "development",
        }
    )
