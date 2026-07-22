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

    # --- Security -----------------------------------------------------------
    _secret = os.environ.get("SECRET_KEY")
    if _secret:
        SECRET_KEY = _secret
    elif DEBUG:
        SECRET_KEY = "dev-key-change-me"
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable is required. "
            "Set it in .env or export it before starting the app."
        )