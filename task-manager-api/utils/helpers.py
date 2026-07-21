"""Shared utility functions used across the project."""

from datetime import datetime
import re


def format_date(date_obj):
    """Format a datetime as string, or return ``None``."""
    if date_obj:
        return str(date_obj)
    return None


def calculate_percentage(part, total):
    """Return ``round((part / total) * 100, 2)``, or 0 if *total* is 0."""
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def validate_email(email):
    """Return ``True`` if *email* looks like a valid email address."""
    return bool(re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email))


def sanitize_string(s):
    """Strip whitespace from *s*, or return ``None``."""
    return s.strip() if s else s


def generate_id():
    """Return a new UUID4 hex string."""
    import uuid
    return str(uuid.uuid4())


def log_action(action, details=None):
    """Print a timestamped log line (transitional — replace with ``logging``)."""
    timestamp = datetime.utcnow()
    print(f"[{timestamp}] ACTION: {action}")
    if details:
        print(f"  DETAILS: {details}")


def parse_date(date_string):
    """Parse a date string in ``YYYY-MM-DD`` or ``DD/MM/YYYY`` format."""
    if not date_string:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    return None


def is_valid_color(color):
    """Return ``True`` if *color* is a 7-char hex string starting with ``#``."""
    return bool(color and len(color) == 7 and color[0] == "#")


def process_task_data(data, existing_task=None):
    """Validate and clean task data dict.

    Returns ``(cleaned_dict, None)`` or ``(None, error_message)``.
    """
    result = {}

    if "title" in data:
        title = data["title"]
        if not title:
            return None, "Título não pode ser vazio"
        title = title.strip()
        if not (3 <= len(title) <= 200):
            return None, "Título deve ter entre 3 e 200 caracteres"
        result["title"] = title

    if "description" in data:
        result["description"] = data["description"]

    if "status" in data:
        valid = {"pending", "in_progress", "done", "cancelled"}
        if data["status"] not in valid:
            return None, "Status inválido"
        result["status"] = data["status"]

    if "priority" in data:
        try:
            p = int(data["priority"])
            if not (1 <= p <= 5):
                return None, "Prioridade deve ser entre 1 e 5"
            result["priority"] = p
        except (ValueError, TypeError):
            return None, "Prioridade inválida"

    if "due_date" in data:
        if data["due_date"]:
            parsed = parse_date(data["due_date"])
            if not parsed:
                return None, "Data inválida"
            result["due_date"] = parsed
        else:
            result["due_date"] = None

    if "tags" in data:
        tags = data["tags"]
        result["tags"] = ",".join(tags) if isinstance(tags, list) else tags

    return result, None


# Named constants used by multiple modules
VALID_STATUSES = frozenset({"pending", "in_progress", "done", "cancelled"})
VALID_ROLES = frozenset({"user", "admin", "manager"})
MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MIN_PASSWORD_LENGTH = 4
DEFAULT_PRIORITY = 3
DEFAULT_COLOR = "#000000"