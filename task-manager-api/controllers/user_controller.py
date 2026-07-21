"""Orchestration layer for User endpoints."""

from flask import jsonify
from services.user_service import UserService


class UserController:
    """Handles user HTTP request/response logic."""

    @staticmethod
    def get_all():
        return jsonify(UserService.get_all_users()), 200

    @staticmethod
    def get_by_id(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(user.to_dict()), 200

    @staticmethod
    def get_tasks(user_id):
        tasks, error = UserService.get_user_tasks(user_id)
        if error:
            return jsonify({"error": error}), 404
        return jsonify(tasks), 200

    @staticmethod
    def create(data):
        user, error = UserService.create_user(data)
        if error:
            return jsonify({"error": error}), 400
        return jsonify(user.to_dict()), 201

    @staticmethod
    def update(user_id, data):
        user, error = UserService.update_user(user_id, data)
        if error:
            status = 404 if error == "Usuário não encontrado" else 400
            return jsonify({"error": error}), status
        return jsonify(user.to_dict()), 200

    @staticmethod
    def delete(user_id):
        success, error = UserService.delete_user(user_id)
        if not success:
            status = 404 if error == "Usuário não encontrado" else 500
            return jsonify({"error": error}), status
        return jsonify({"message": "Usuário deletado com sucesso"}), 200

    @staticmethod
    def login(data):
        response, status = UserService.login(data)
        return jsonify(response), status