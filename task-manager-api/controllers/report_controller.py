"""Orchestration layer for Report endpoints."""

from flask import jsonify
from services.report_service import ReportService


class ReportController:
    """Handles report HTTP request/response logic."""

    @staticmethod
    def summary():
        return jsonify(ReportService.summary_report()), 200

    @staticmethod
    def user_report(user_id):
        report, error = ReportService.user_report(user_id)
        if error:
            return jsonify({"error": error}), 404
        return jsonify(report), 200