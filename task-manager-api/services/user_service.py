"""Business logic for User operations."""

import re
from database import db
from models.user import User
from models.task import Task
from datetime import datetime


class UserService:
    """Encapsulates all user-related business rules and database access."""

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    VALID_ROLES = frozenset({"user", "admin", "manager"})
    EMAIL_RE = re.compile(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")
    MIN_PASSWORD_LENGTH = 4

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    @staticmethod
    def get_all_users():
        """Return a list of user summaries (without password hashes)."""
        users = User.query.all()
        result = []
        for u in users:
            result.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "active": u.active,
                "created_at": str(u.created_at),
                "task_count": len(u.tasks),
            })
        return result

    @staticmethod
    def get_user_by_id(user_id):
        """Return the full user dict (without password) or ``None``."""
        user = User.query.get(user_id)
        return user

    @staticmethod
    def get_user_tasks(user_id):
        """Return a list of task dicts for a given user, with overdue flag."""
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado"

        tasks = Task.query.filter_by(user_id=user_id).all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data["overdue"] = t.is_overdue()
            result.append(task_data)
        return result, None

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    @staticmethod
    def create_user(data):
        """Validate *data* and create a new user.

        Returns ``(user, None)`` on success or ``(None, error_message)`` on
        validation / database failure.
        """
        if not data:
            return None, "Dados inválidos"

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        # --- field-level validation ----------------------------------------
        if not name:
            return None, "Nome é obrigatório"
        if not email:
            return None, "Email é obrigatório"
        if not password:
            return None, "Senha é obrigatória"

        if not UserService.EMAIL_RE.match(email):
            return None, "Email inválido"
        if len(password) < UserService.MIN_PASSWORD_LENGTH:
            return None, "Senha deve ter no mínimo 4 caracteres"
        if role not in UserService.VALID_ROLES:
            return None, "Role inválido"

        # --- duplicate check -----------------------------------------------
        if User.query.filter_by(email=email).first():
            return None, "Email já cadastrado"

        # --- persist -------------------------------------------------------
        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception:
            db.session.rollback()
            return None, "Erro ao criar usuário"

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    @staticmethod
    def update_user(user_id, data):
        """Validate and update user fields.

        Returns ``(user, None)`` on success or ``(None, error_message)``.
        """
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado"
        if not data:
            return None, "Dados inválidos"

        # --- email ---------------------------------------------------------
        if "email" in data:
            if not UserService.EMAIL_RE.match(data["email"]):
                return None, "Email inválido"
            existing = User.query.filter_by(email=data["email"]).first()
            if existing and existing.id != user_id:
                return None, "Email já cadastrado"
            user.email = data["email"]

        # --- name ----------------------------------------------------------
        if "name" in data:
            user.name = data["name"]

        # --- password ------------------------------------------------------
        if "password" in data:
            if len(data["password"]) < UserService.MIN_PASSWORD_LENGTH:
                return None, "Senha muito curta"
            user.set_password(data["password"])

        # --- role ----------------------------------------------------------
        if "role" in data:
            if data["role"] not in UserService.VALID_ROLES:
                return None, "Role inválido"
            user.role = data["role"]

        # --- active --------------------------------------------------------
        if "active" in data:
            user.active = data["active"]

        # --- persist -------------------------------------------------------
        try:
            db.session.commit()
            return user, None
        except Exception:
            db.session.rollback()
            return None, "Erro ao atualizar"

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------
    @staticmethod
    def delete_user(user_id):
        """Delete a user and all their tasks.

        Returns ``(True, None)`` on success or ``(False, error_message)``.
        """
        user = User.query.get(user_id)
        if not user:
            return False, "Usuário não encontrado"

        # Remove associated tasks first
        Task.query.filter_by(user_id=user_id).delete()

        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception:
            db.session.rollback()
            return False, "Erro ao deletar"

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------
    @staticmethod
    def login(data):
        """Authenticate a user by email + password.

        Returns ``(response_dict, status_code)``.
        """
        if not data:
            return {"error": "Dados inválidos"}, 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email e senha são obrigatórios"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"error": "Credenciais inválidas"}, 401

        if not user.active:
            return {"error": "Usuário inativo"}, 403

        return {
            "message": "Login realizado com sucesso",
            "user": user.to_dict(),
            "token": "fake-jwt-token-" + str(user.id),
        }, 200