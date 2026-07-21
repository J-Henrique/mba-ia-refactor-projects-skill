"""Orchestration layer for Task endpoints.

Controllers receive parsed request data, call the appropriate service, and
return Flask Response objects.  They are the bridge between HTTP (routes)
and business logic (services).
"""

from flask import jsonify
from services.task_service import TaskService


class TaskController:
    """Handles task HTTP request/response logic."""

    @staticmethod
    def get_all():
        try:
            return jsonify(TaskService.get_all_tasks()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_by_id(task_id):
        task = TaskService.get_task_by_id(task_id)
        if task:
            return jsonify(task), 200
        return jsonify({"error": "Task não encontrada"}), 404

    @staticmethod
    def create(data):
        try:
            task = TaskService.create_task(data)
            return jsonify(task.to_dict()), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "Erro ao criar task"}), 500

    @staticmethod
    def update(task_id, data):
        try:
            task = TaskService.update_task(task_id, data)
            if task:
                return jsonify(task.to_dict()), 200
            return jsonify({"error": "Task não encontrada"}), 404
        except Exception:
            return jsonify({"error": "Erro ao atualizar"}), 500

    @staticmethod
    def delete(task_id):
        if TaskService.delete_task(task_id):
            return jsonify({"message": "Task deletada com sucesso"}), 200
        return jsonify({"error": "Task não encontrada"}), 404

    @staticmethod
    def search(params):
        return jsonify(TaskService.search_tasks(params)), 200

    @staticmethod
    def stats():
        return jsonify(TaskService.get_stats()), 200