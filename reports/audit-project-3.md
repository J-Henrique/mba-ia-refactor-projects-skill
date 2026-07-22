---
# ARCHITECTURE AUDIT REPORT
Project: task-manager-api
Stack: Python + Flask + SQLAlchemy/SQLite
Files: 14 source files analyzed | ~1015 lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 5 | LOW: 3

## Findings

### [CRITICAL] Hardcoded Credentials
File: services/notification_service.py:9-10
Description: SMTP email credentials (`email_user = 'taskmanager@gmail.com'`, `email_password = 'senha123'`) are hardcoded in the class constructor.
Impact: If committed to a public repository, credentials are exposed to anyone with access to the codebase.
Recommendation: Move credentials to environment variables: `os.environ.get('SMTP_USER')` / `os.environ.get('SMTP_PASSWORD')` with a `.env` file for local development.

### [CRITICAL] Deprecated API Usage (MD5 Password Hashing)
File: models/user.py:29,32
Description: `hashlib.md5()` is used for password hashing. MD5 is cryptographically broken and unsuitable for password storage.
Impact: If the database is compromised, all user passwords can be trivially reversed.
Recommendation: Replace with `werkzeug.security.generate_password_hash()` / `check_password_hash()` (uses bcrypt/scrypt by default).

### [HIGH] Fat Controller (Fat Routes)
File: routes/user_routes.py:10-211
Description: The `user_routes.py` file contains all business logic mixed with request handling: validation, DB queries, error handling, and response formatting are all inline. No service layer is used for users.
Impact: Routes are impossible to unit-test without HTTP requests, business logic cannot be reused, and the file is difficult to maintain.
Recommendation: Extract business logic to a `UserService` class in `services/`, leaving only request parsing and response formatting in the route.

### [HIGH] Fat Controller (Fat Routes)
File: routes/report_routes.py:12-223
Description: The `report_routes.py` file mixes report generation logic, category CRUD operations, and N+1 query patterns. Category routes are misplaced in a file named `report_routes`.
Impact: Same as above — untestable, unreusable, mixed responsibilities.
Recommendation: Extract category CRUD to a dedicated `CategoryService` in `services/` and report logic to a `ReportService`. Consider moving category routes to a separate blueprint.

### [HIGH] Tight Coupling
File: routes/user_routes.py:2-5, routes/report_routes.py:2-5
Description: Both `user_routes.py` and `report_routes.py` import `db` directly from `database.py` and perform raw SQLAlchemy operations inline, bypassing the service layer.
Impact: Tight coupling to the database implementation makes it impossible to swap databases or unit-test business logic without a real database.
Recommendation: Route files should only import and call service methods. All database access should be encapsulated in models/services.

### [MEDIUM] N+1 Queries
File: services/task_service.py:15-16
Description: `get_all_tasks()` performs individual `User.query.get()` and `Category.query.get()` queries for each task in a loop.
Impact: With N tasks, this executes 1 + 2N queries instead of 3 total. At 100 tasks, that's 201 queries instead of 3.
Recommendation: Use SQLAlchemy eager loading (`joinedload()` or `selectinload()`) on the relationships.

### [MEDIUM] N+1 Queries
File: routes/report_routes.py:33-43,55-68
Description: The summary report iterates all tasks to calculate overdue counts and loops over all users to compute task stats, each with individual queries.
Impact: Same as above — performance degrades linearly with data size.
Recommendation: Use aggregate queries (`GROUP BY`, `func.count()`) at the database level instead of in-memory iteration.

### [MEDIUM] Duplicate Code — Overdue Logic
File: models/task.py:50-60, routes/user_routes.py:171-180, routes/report_routes.py:34-43,132-135, services/task_service.py:101
Description: The overdue calculation logic (`if due_date and due_date < now and status not in ['done','cancelled']`) is repeated in at least 5 locations across the codebase.
Impact: If the overdue business rule changes (e.g., adding a grace period), all 5 locations must be updated in sync.
Recommendation: Consolidate into a single method on the `Task` model (already exists as `is_overdue()`) and reuse it everywhere.

### [MEDIUM] Mixed Responsibilities (Misplaced Routes)
File: routes/report_routes.py:157-223
Description: Category CRUD endpoints (`/categories`, `/categories/<id>`) are defined in `report_routes.py`, not in a dedicated category blueprint.
Impact: Violates separation of concerns; confusing for developers.
Recommendation: Create a dedicated `category_routes.py` blueprint and a `CategoryService` in services.

### [MEDIUM] Hardcoded Fallback Secret
File: app.py:16
Description: `SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')` — while the env var is checked first, the fallback value is a weak default.
Impact: If deployed without setting the env var, the session secret is trivially guessable.
Recommendation: Remove the fallback default, or raise an error if `SECRET_KEY` is not set in production.

### [LOW] Print Statements Instead of Logging
File: routes/user_routes.py:83,89,147, services/notification_service.py:21,24
Description: `print()` is used for logging instead of Python's `logging` module.
Impact: No log levels, no structured output, no configurable destinations.
Recommendation: Replace `print()` with `app.logger` or a dedicated `logging` configuration.

### [LOW] Inconsistent Naming
File: routes/report_routes.py
Description: The file is named `report_routes.py` but contains both report and category endpoints. Magic numbers like `4`, `3`, `200` are used instead of named constants.
Impact: Reduces readability and maintainability.
Recommendation: Rename/extract to appropriate files and replace magic numbers with named constants.

### [LOW] Unused Imports
File: models/task.py:3, routes/report_routes.py:8, utils/helpers.py:4-8
Description: Several unused imports: `json` in `task.py` and `report_routes.py`, `os`, `json`, `sys`, `math`, `hashlib` in `helpers.py`.
Impact: Minor — adds noise and marginal overhead.
Recommendation: Remove unused imports.

---
Total: 13 findings
---

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]