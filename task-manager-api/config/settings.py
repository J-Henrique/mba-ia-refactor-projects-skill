"""Centralized application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration.

    All secrets and environment-specific values are loaded from environment
    variables.  A missing ``SECRET_KEY`` raises in production so the app
    never runs with a weak default; in development (``DEBUG=true``) it
    falls back to a safe-for-dev default.
    """

    # --- Debug -------------------------------------------------------------
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

    # --- Database -----------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///tasks.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Security -----------------------------------------------------------
    _secret = os.environ.get("SECRET_KEY")
    if _secret:
        SECRET_KEY = _secret
    elif DEBUG:
        SECRET_KEY = "dev-secret-key-change-in-production"
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable is required. "
            "Set it in .env or export it before starting the app."
        )

    # --- SMTP (email notifications) -----------------------------------------
    SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")