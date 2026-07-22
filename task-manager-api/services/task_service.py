"""Business logic for Task operations."""

from database import db
from models.task import Task
from datetime import datetime, timezone
from sqlalchemy.orm import joinedload
from sqlalchemy import func


class TaskService:
    """Encapsulates all task-related business rules and database access."""

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------
    @staticmethod
    def get_all_tasks():
        """Return all tasks with user/category names via eager loading.

        Uses ``joinedload`` to avoid the N+1 query anti-pattern: the
        previous version queried User and Category individually for each
        task in a loop (1 + 2N queries).
        """
        tasks = (
            Task.query
            .options(joinedload(Task.user), joinedload(Task.category))
            .all()
        )
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data["overdue"] = t.is_overdue()
            task_data["user_name"] = t.user.name if t.user else None
            task_data["category_name"] = t.category.name if t.category else None
            result.append(task_data)
        return result

    @staticmethod
    def get_task_by_id(task_id):
        """Return a single task dict (with overdue flag) or ``None``."""
        task = (
            Task.query
            .options(joinedload(Task.user), joinedload(Task.category))
            .get(task_id)
        )
        if not task:
            return None
        data = task.to_dict()
        data["overdue"] = task.is_overdue()
        return data

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------
    @staticmethod
    def create_task(data):
        """Validate *data* and create a new task.

        Returns the ``Task`` instance or raises ``ValueError``.
        """
        title = data.get("title")
        if not title or len(title) < 3 or len(title) > 200:
            raise ValueError("Título inválido")

        task = Task(
            title=title,
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            priority=data.get("priority", 3),
            user_id=data.get("user_id"),
            category_id=data.get("category_id"),
        )
        if data.get("due_date"):
            task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d")
        if data.get("tags"):
            tags = data["tags"]
            task.tags = (
                ",".join(tags) if isinstance(tags, list) else tags
            )

        db.session.add(task)
        db.session.commit()
        return task

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    @staticmethod
    def update_task(task_id, data):
        """Update a task.  Returns the ``Task`` or ``None`` if not found."""
        task = Task.query.get(task_id)
        if not task:
            return None

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        if "priority" in data:
            task.priority = data["priority"]
        if "due_date" in data:
            task.due_date = (
                datetime.strptime(data["due_date"], "%Y-%m-%d")
                if data["due_date"]
                else None
            )

        task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.session.commit()
        return task

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------
    @staticmethod
    def delete_task(task_id):
        """Delete a task.  Returns ``True`` if found, else ``False``."""
        task = Task.query.get(task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    @staticmethod
    def search_tasks(query_params):
        """Filter tasks by optional ``q`` (text) and ``status`` params."""
        query = Task.query
        if "q" in query_params:
            q = query_params["q"]
            query = query.filter(
                Task.title.like(f"%{q}%")
                | Task.description.like(f"%{q}%")
            )
        if "status" in query_params:
            query = query.filter(Task.status == query_params["status"])

        return [t.to_dict() for t in query.all()]

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    @staticmethod
    def get_stats():
        """Aggregate task statistics using database-level queries."""
        total = Task.query.count()
        done = Task.query.filter_by(status="done").count()
        pending = Task.query.filter_by(status="pending").count()
        now = datetime.now(timezone.utc)
        overdue = (
            Task.query.filter(
                Task.due_date.isnot(None),
                Task.due_date < now,
                Task.status.notin_(["done", "cancelled"]),
            ).count()
        )

        return {
            "total": total,
            "pending": pending,
            "done": done,
            "overdue": overdue,
            "completion_rate": round((done / total) * 100, 2)
            if total > 0
            else 0,
        }