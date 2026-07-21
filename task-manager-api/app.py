"""Application entry point.

Creates the Flask app, loads configuration, registers blueprints, and
attaches error handlers.
"""

import logging
import datetime
from flask import Flask
from flask_cors import CORS
from database import db
from config.settings import Config
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.report_routes import report_bp
from routes.category_routes import category_bp
from utils.error_handler import register_error_handlers

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

# Register error handlers early so they catch blueprint errors too.
register_error_handlers(app)

# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------
app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)
app.register_blueprint(category_bp)


# ---------------------------------------------------------------------------
# Built-in routes
# ---------------------------------------------------------------------------
@app.route("/health")
def health():
    return {
        "status": "ok",
        "timestamp": str(datetime.datetime.now(datetime.timezone.utc)),
    }


@app.route("/")
def index():
    return {"message": "Task Manager API", "version": "1.0"}


# ---------------------------------------------------------------------------
# Initialise database tables
# ---------------------------------------------------------------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)