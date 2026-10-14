"""
config.py – Configuration and Environment Settings for CyberSentinel AI
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cybersentinel-enterprise-soc-token-key-2026")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    PORT = int(os.getenv("FLASK_PORT", 5000))
    DEBUG = os.getenv("FLASK_ENV", "development").lower() == "development"

    # Risk thresholds
    ANOMALY_THRESHOLD = 0.65
    HIGH_SEVERITY_THRESHOLD = 7.5
