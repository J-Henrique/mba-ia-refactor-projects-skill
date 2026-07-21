"""Report API endpoints — thin layer that delegates to the controller."""

from flask import Blueprint, jsonify
from controllers.report_controller import ReportController

report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports/summary", methods=["GET"])
def summary_report():
    return ReportController.summary()


@report_bp.route("/reports/user/<int:user_id>", methods=["GET"])
def user_report(user_id):
    return ReportController.user_report(user_id)