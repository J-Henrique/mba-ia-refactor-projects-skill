"""Centralized error handling middleware.

Replaces ad-hoc ``try/except`` blocks scattered across routes with
Flask error handlers that return consistent JSON responses.
"""

import logging
import traceback
from flask import jsonify

# Module-level logger — the app can configure its level / handler.
logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Attach standard JSON error handlers to the Flask *app*."""

    @app.errorhandler(400)
    def bad_request(exc):
        logger.warning("Bad request: %s", exc)
        return jsonify({"error": str(exc) or "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(exc):
        logger.info("Not found: %s", exc)
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(exc):
        logger.warning("Method not allowed: %s", exc)
        return jsonify({"error": "Método não permitido"}), 405

    @app.errorhandler(422)
    def unprocessable(exc):
        logger.warning("Unprocessable entity: %s", exc)
        return jsonify({"error": str(exc) or "Entidade não processável"}), 422

    @app.errorhandler(500)
    def internal_error(exc):
        logger.error("Internal server error: %s", exc)
        logger.debug(traceback.format_exc())
        return jsonify({"error": "Erro interno do servidor"}), 500

    # Catch-all for anything that isn't an HTTPException (e.g.    plain
    # ``raise`` in a view function).  Flask converts those to 500
    # internally, but we log the traceback here for debugging.
    @app.errorhandler(Exception)
    def unhandled(exc):
        logger.critical("Unhandled exception: %s", exc)
        logger.debug(traceback.format_exc())
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app