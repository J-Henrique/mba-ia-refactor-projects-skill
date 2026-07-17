from flask import Blueprint, request, jsonify
from services.task_service import TaskService

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        return jsonify(TaskService.get_all_tasks()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskService.get_task_by_id(task_id)
    return jsonify(task) if task else (jsonify({'error': 'Task não encontrada'}), 404)

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        task = TaskService.create_task(request.get_json())
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao criar task'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = TaskService.update_task(task_id, request.get_json())
        return jsonify(task.to_dict()) if task else (jsonify({'error': 'Task não encontrada'}), 404)
    except Exception as e:
        return jsonify({'error': 'Erro ao atualizar'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if TaskService.delete_task(task_id):
        return jsonify({'message': 'Task deletada com sucesso'}), 200
    return jsonify({'error': 'Task não encontrada'}), 404

@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    return jsonify(TaskService.search_tasks(request.args)), 200

@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    return jsonify(TaskService.get_stats()), 200
