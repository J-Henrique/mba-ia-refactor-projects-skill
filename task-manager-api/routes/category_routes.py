"""Category API endpoints — thin layer that delegates to the controller."""

from flask import Blueprint, request, jsonify
from controllers.category_controller import CategoryController

category_bp = Blueprint("categories", __name__)


@category_bp.route("/categories", methods=["GET"])
def get_categories():
    return CategoryController.get_all()


@category_bp.route("/categories", methods=["POST"])
def create_category():
    return CategoryController.create(request.get_json())


@category_bp.route("/categories/<int:cat_id>", methods=["PUT"])
def update_category(cat_id):
    return CategoryController.update(cat_id, request.get_json())


@category_bp.route("/categories/<int:cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    return CategoryController.delete(cat_id)