"""Orchestration layer for Category endpoints."""

from flask import jsonify
from services.category_service import CategoryService


class CategoryController:
    """Handles category HTTP request/response logic."""

    @staticmethod
    def get_all():
        return jsonify(CategoryService.get_all_categories()), 200

    @staticmethod
    def create(data):
        cat, error = CategoryService.create_category(data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(cat.to_dict()), 201

    @staticmethod
    def update(cat_id, data):
        cat, error = CategoryService.update_category(cat_id, data)
        if error:
            status = 404 if "não encontrada" in error else 400
            return jsonify({"error": error}), status
        return jsonify(cat.to_dict()), 200

    @staticmethod
    def delete(cat_id):
        success, error = CategoryService.delete_category(cat_id)
        if not success:
            status = 404 if "não encontrada" in error else 500
            return jsonify({"error": error}), status
        return jsonify({"message": "Categoria deletada"}), 200