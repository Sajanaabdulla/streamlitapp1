"""
config.py — Central Configuration File
========================================
Think of this file as the "settings panel" of your app.
All sensitive values (API keys, DB passwords) are read from
a .env file so they are never hardcoded in your source code.

HOW TO USE:
  1. Create a file called  .env  in the backend/ folder.
  2. Fill in your real values (see the template below).
  3. This file reads those values automatically.

.env template:
-------------------------------------------------
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=helio_solar_db
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=some_random_secret_string
-------------------------------------------------
"""

import os
from dotenv import load_dotenv

# Load values from the .env file into environment variables
load_dotenv()


class Config:
    """
    Base configuration class.
    All settings live here as class-level attributes so every
    part of the app can import and read them from one place.
    """

    # ── Flask ──────────────────────────────────────────────
    # SECRET_KEY is used internally by Flask for security tokens.
    SECRET_KEY = os.getenv("SECRET_KEY", "helio-solar-secret-2024")

    # Debug mode: True shows detailed error pages during development.
    # ALWAYS set this to False in production!
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # ── MySQL Database ─────────────────────────────────────
    MYSQL_HOST     = os.getenv("MYSQL_HOST",     "localhost")
    MYSQL_USER     = os.getenv("MYSQL_USER",     "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "helio_solar_db")
    MYSQL_PORT     = int(os.getenv("MYSQL_PORT", 3306))

    # ── Google Gemini AI ──────────────────────────────────
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    # The specific Gemini model we want to use
    GEMINI_MODEL   = "gemini-1.5-flash"

    # ── File Upload Settings ──────────────────────────────
    # Folder where uploaded rooftop images and bills are stored
    UPLOAD_FOLDER        = os.path.join(os.path.dirname(__file__), "uploads")
    # Maximum file size: 16 MB (16 * 1024 * 1024 bytes)
    MAX_CONTENT_LENGTH   = 16 * 1024 * 1024
    # Only these file types are allowed for uploads
    ALLOWED_IMAGE_EXT    = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_BILL_EXT     = {"pdf", "png", "jpg", "jpeg"}

    # ── ML Model ──────────────────────────────────────────
    # Primary XGBoost pipeline; legacy bundle path kept as fallback
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__), "models", "xgboost_solar_model.joblib"
    )
    LEGACY_MODEL_PATH = os.path.join(
        os.path.dirname(__file__), "models", "solar_model.pkl"
    )

    # ── Dataset ───────────────────────────────────────────
    DATASET_PATH = os.path.join(os.path.dirname(__file__), "datasets", "solar_dataset.csv")

    # ── Solar Calculation Constants ───────────────────────
    # Average solar panel efficiency (20%)
    PANEL_EFFICIENCY    = 0.20
    # Performance ratio — accounts for real-world losses (dust, wiring, etc.)
    PERFORMANCE_RATIO   = 0.80
    # Typical solar panel size in square meters (1 kW ≈ 6 m²)
    SQM_PER_KW          = 6.0
    # Average cost per kW installed in India (₹)
    COST_PER_KW         = 65000
    # Average KSEB electricity tariff (₹ per unit / kWh)
    ELECTRICITY_TARIFF  = 6.50
    # System lifetime for ROI calculations (years)
    SYSTEM_LIFETIME_YEARS = 25

    # Supported cities in the Streamlit UI (dataset city in parentheses)
    SUPPORTED_CITIES = [
        "Thiruvananthapuram",
        "Kochi",
        "Bengaluru",
        "Mumbai",
        "Delhi",
        "Madhya Pradesh",
    ]
    # Map display name → NASA POWER dataset city label
    CITY_DATASET_MAP = {
        "Madhya Pradesh": "Bhopal",
    }

    # ── CORS (Cross-Origin Resource Sharing) ─────────────
    # This allows your React frontend (running on a different port)
    # to communicate with this Flask backend.
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]


class DevelopmentConfig(Config):
    """Settings for local development — more verbose logging."""
    DEBUG = True


class ProductionConfig(Config):
    """Settings for live deployment — debug OFF for security."""
    DEBUG = False


# This dictionary lets app.py pick the right config by name
config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}
