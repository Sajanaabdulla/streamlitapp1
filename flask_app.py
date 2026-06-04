"""
flask_app.py — Flask REST API (optional backend)
=================================================
Run with:  python flask_app.py

The primary user interface is the Streamlit app (app.py).
This Flask server remains available for API integrations.
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database.db import init_db_pool, test_connection
from routes.solar_routes import solar_bp
from routes.chatbot_routes import chatbot_bp
from routes.bill_routes import bill_bp
from routes.upload_routes import upload_bp
from routes.report_routes import report_bp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "models"), exist_ok=True)

    CORS(
        app,
        resources={r"/api/*": {"origins": Config.CORS_ORIGINS}},
        supports_credentials=True,
    )

    try:
        init_db_pool()
    except Exception as e:
        logger.warning("DB pool init failed: %s", e)

    app.register_blueprint(solar_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")
    app.register_blueprint(bill_bp, url_prefix="/api")
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({
            "message": "HelioSense AI API is running",
            "streamlit": "Run: streamlit run app.py",
        })

    @app.route("/api/health")
    def health_check():
        db_ok = test_connection()
        return jsonify({
            "status": "healthy" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
            "app": "HelioSense AI",
        }), (200 if db_ok else 503)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
