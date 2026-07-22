"""Business logic for Report generation."""

from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime, timedelta, timezone
from sqlalchemy import func


class ReportService:
    """Aggregation and report queries — all database-level, no in-memory loops."""

    # ------------------------------------------------------------------
    # Summary report
    # ------------------------------------------------------------------
    @staticmethod
    def summary_report():
        """Build the full summary report dict."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        seven_days_ago = now - timedelta(days=7)

        # --- counts --------------------------------------------------------
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        # --- status breakdown ----------------------------------------------
        status_counts = dict(
            db.session.query(Task.status, func.count(Task.id))
            .group_by(Task.status)
            .all()
        )

        # --- priority breakdown --------------------------------------------
        priority_counts = dict(
            db.session.query(Task.priority, func.count(Task.id))
            .group_by(Task.priority)
            .all()
        )

        # --- overdue tasks (efficient filter, not in-memory) ---------------
        overdue_tasks = (
            Task.query.filter(
                Task.due_date.isnot(None),
                Task.due_date < now,
                Task.status.notin_(["done", "cancelled"]),
            )
            .all()
        )
        overdue_count = len(overdue_tasks)
        overdue_list = [
            {
                "id": t.id,
                "title": t.title,
                "due_date": str(t.due_date),
                "days_overdue": (now - t.due_date).days,
            }
            for t in overdue_tasks
        ]

        # --- recent activity -----------------------------------------------
        recent_tasks = Task.query.filter(
            Task.created_at >= seven_days_ago
        ).count()

        recent_done = Task.query.filter(
            Task.status == "done", Task.updated_at >= seven_days_ago
        ).count()

        # --- per-user productivity -----------------------------------------
        users = User.query.all()
        user_stats = []
        for u in users:
            total = Task.query.filter_by(user_id=u.id).count()
            completed = (
                Task.query.filter_by(user_id=u.id, status="done").count()
            )
            user_stats.append({
                "user_id": u.id,
                "user_name": u.name,
                "total_tasks": total,
                "completed_tasks": completed,
                "completion_rate": round((completed / total) * 100, 2)
                if total > 0
                else 0,
            })

        return {
            "generated_at": str(now),
            "overview": {
                "total_tasks": total_tasks,
                "total_users": total_users,
                "total_categories": total_categories,
            },
            "tasks_by_status": {
                "pending": status_counts.get("pending", 0),
                "in_progress": status_counts.get("in_progress", 0),
                "done": status_counts.get("done", 0),
                "cancelled": status_counts.get("cancelled", 0),
            },
            "tasks_by_priority": {
                "critical": priority_counts.get(1, 0),
                "high": priority_counts.get(2, 0),
                "medium": priority_counts.get(3, 0),
                "low": priority_counts.get(4, 0),
                "minimal": priority_counts.get(5, 0),
            },
            "overdue": {
                "count": overdue_count,
                "tasks": overdue_list,
            },
            "recent_activity": {
                "tasks_created_last_7_days": recent_tasks,
                "tasks_completed_last_7_days": recent_done,
            },
            "user_productivity": user_stats,
        }

    # ------------------------------------------------------------------
    # Per-user report
    # ------------------------------------------------------------------
    @staticmethod
    def user_report(user_id):
        """Build a report for a single user.

        Returns ``(report_dict, None)`` or ``(None, error_message)``.
        """
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado"

        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        done = sum(1 for t in tasks if t.status == "done")
        pending = sum(1 for t in tasks if t.status == "pending")
        in_progress = sum(1 for t in tasks if t.status == "in_progress")
        cancelled = sum(1 for t in tasks if t.status == "cancelled")
        overdue = sum(1 for t in tasks if t.is_overdue())
        high_priority = sum(1 for t in tasks if t.priority <= 2)

        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "statistics": {
                "total_tasks": total,
                "done": done,
                "pending": pending,
                "in_progress": in_progress,
                "cancelled": cancelled,
                "overdue": overdue,
                "high_priority": high_priority,
                "completion_rate": round((done / total) * 100, 2)
                if total > 0
                else 0,
            },
        }, None