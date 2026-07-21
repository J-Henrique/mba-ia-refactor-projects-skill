"""Business logic for Category operations."""

from database import db
from models.category import Category
from models.task import Task


class CategoryService:
    """Encapsulates all category-related business rules and database access."""

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    @staticmethod
    def get_all_categories():
        """Return a list of categories with task counts."""
        categories = Category.query.all()
        result = []
        for c in categories:
            cat_data = c.to_dict()
            cat_data["task_count"] = Task.query.filter_by(category_id=c.id).count()
            result.append(cat_data)
        return result

    @staticmethod
    def get_category_by_id(cat_id):
        """Return a category or ``None``."""
        return Category.query.get(cat_id)

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    @staticmethod
    def create_category(data):
        """Validate and create a category.

        Returns ``(category, None)`` or ``(None, error_message)``.
        """
        if not data:
            return None, "Dados inválidos"

        name = data.get("name")
        if not name:
            return None, "Nome é obrigatório"

        category = Category()
        category.name = name
        category.description = data.get("description", "")
        category.color = data.get("color", "#000000")

        try:
            db.session.add(category)
            db.session.commit()
            return category, None
        except Exception:
            db.session.rollback()
            return None, "Erro ao criar categoria"

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    @staticmethod
    def update_category(cat_id, data):
        """Update a category.

        Returns ``(category, None)`` or ``(None, error_message)``.
        """
        cat = Category.query.get(cat_id)
        if not cat:
            return None, "Categoria não encontrada"
        if not data:
            return None, "Dados inválidos"

        if "name" in data:
            cat.name = data["name"]
        if "description" in data:
            cat.description = data["description"]
        if "color" in data:
            cat.color = data["color"]

        try:
            db.session.commit()
            return cat, None
        except Exception:
            db.session.rollback()
            return None, "Erro ao atualizar"

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------
    @staticmethod
    def delete_category(cat_id):
        """Delete a category.

        Returns ``(True, None)`` or ``(False, error_message)``.
        """
        cat = Category.query.get(cat_id)
        if not cat:
            return False, "Categoria não encontrada"

        try:
            db.session.delete(cat)
            db.session.commit()
            return True, None
        except Exception:
            db.session.rollback()
            return False, "Erro ao deletar"