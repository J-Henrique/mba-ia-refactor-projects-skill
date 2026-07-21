"""User API endpoints — thin layer that delegates to the controller."""

from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    return UserController.get_all()


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return UserController.get_by_id(user_id)


@user_bp.route("/users/<int:user_id>/tasks", methods=["GET"])
def get_user_tasks(user_id):
    return UserController.get_tasks(user_id)


@user_bp.route("/users", methods=["POST"])
def create_user():
    return UserController.create(request.get_json())


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    return UserController.update(user_id, request.get_json())


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    return UserController.delete(user_id)


@user_bp.route("/login", methods=["POST"])
def login():
    return UserController.login(request.get_json())