# ARCHITECTURE AUDIT REPORT
Project: ecommerce-api-legacy
Stack: Node.js + Express
Files: 3 analyzed | ~181 lines of code

## Summary
CRITICAL: 3 | HIGH: 2 | MEDIUM: 4 | LOW: 2

## Findings

### [CRITICAL] Hardcoded Credentials
File: src/utils.js:2-6
Description: Database credentials, payment gateway key, and SMTP credentials are hardcoded directly in the source code. The `config` object exposes `dbUser`, `dbPass`, `paymentGatewayKey`, and `smtpUser` as plaintext strings. These secrets are also present in `.env.example` but the running code reads from `utils.js`, not from environment variables.
Impact: If this code is committed to a public repository or shared with third parties, all production credentials are exposed. A malicious actor could access the database, payment gateway, or SMTP server.
Recommendation: Move all credentials to environment variables, read them via `process.env` at application startup, and use the `dotenv` package (already in dependencies) to load `.env` in development. Remove hardcoded secrets from `utils.js` and delete them from `.env.example` (replace with placeholder values).

### [CRITICAL] God Class
File: src/AppManager.js:1-141
Description: The `AppManager` class is a monolithic god class containing ALL application logic: database initialization (lines 10-21), HTTP route definitions (lines 25-138), checkout business logic with payment processing (lines 28-78), financial report generation with nested queries (lines 80-129), and user deletion (lines 131-137). The class handles data persistence, business rules, and HTTP response formatting in a single unit.
Impact: Impossible to unit test individual components. Any change to checkout logic risks breaking routes or database operations. The class cannot be extended or reused without modification.
Recommendation: Split into separate layers: models (database operations), controllers (business logic), routes (HTTP definitions), and services (reusable business operations). Apply dependency injection so the database can be mocked.

### [CRITICAL] Deprecated API Usage / Insecure Cryptography
File: src/utils.js:17-22
Description: The `badCrypto` function implements a custom password hashing algorithm using repeated base64 encoding (10000 iterations, truncated to 10 chars). This is not a cryptographic hash — it is reversible and provides no actual security. Meanwhile, `bcryptjs` is already listed as a dependency in `package.json` but is never imported or used.
Impact: User passwords are stored in a trivially reversible format, not a true cryptographic hash. An attacker who gains database access can recover all plaintext passwords. This is a severe data breach risk.
Recommendation: Replace `badCrypto` with `bcryptjs` (already installed). Use `bcrypt.hashSync()` for password hashing and `bcrypt.compareSync()` for verification. Remove the `badCrypto` function entirely.

### [HIGH] Fat Controller (God Routes)
File: src/AppManager.js:28-78, 80-129
Description: The route handlers in `setupRoutes` contain all business logic inline. The checkout endpoint (lines 28-78) has deeply nested callbacks handling course lookup, user creation/retrieval, payment processing, enrollment creation, payment recording, and audit logging — all within the route definition. The financial report endpoint (lines 80-129) similarly has 4 levels of nested callbacks with manual concurrency tracking.
Impact: Business logic is tightly coupled to HTTP transport. Cannot reuse checkout logic for non-HTTP contexts (CLI, tests, background jobs). Deeply nested callbacks create "callback hell" making the code hard to read and maintain.
Recommendation: Extract business logic into controllers and services. Routes should only parse input and delegate to controllers. Controllers should orchestrate services/models. Use async/await or Promises instead of nested callbacks.

### [HIGH] Tight Coupling
File: src/AppManager.js:7
Description: The `AppManager` class creates its own `sqlite3.Database` instance directly in the constructor (`this.db = new sqlite3.Database(':memory:')`). There is no dependency injection — the database implementation is hardcoded and cannot be swapped or mocked.
Impact: Unit testing is impossible without a real SQLite database. Cannot switch to a different database engine or connection mode without modifying the class. Integration tests are forced to use the same in-memory database.
Recommendation: Accept the database instance as a constructor parameter (`constructor(db) { this.db = db; }`). Create and inject the database from the composition root (`app.js`). This allows mocking in tests and swapping implementations.

### [MEDIUM] N+1 Queries
File: src/AppManager.js:80-129
Description: The financial report endpoint executes queries in a loop pattern: first queries all courses (1 query), then for each course queries enrollments (N queries), then for each enrollment queries users and payments (2N queries). This results in 1 + 3N database queries where a single JOIN query would suffice.
Impact: Performance degrades linearly with the number of courses and enrollments. With 10 courses and 100 enrollments, this endpoint executes ~300+ queries instead of 1-3.
Recommendation: Use SQL JOIN queries with aggregation to fetch all data in 1-2 queries. For example: `SELECT c.title, u.name, u.email, p.amount, p.status FROM courses c LEFT JOIN enrollments e ON c.id = e.course_id LEFT JOIN users u ON e.user_id = u.id LEFT JOIN payments p ON e.id = p.enrollment_id`.

### [MEDIUM] Duplicate Code
File: src/AppManager.js:37-63
Description: The same error handling pattern (`if (err) return res.status(500).send("Erro DB")`) is repeated across every callback. The audit logging pattern (`INSERT INTO audit_logs`) is hardcoded inline rather than abstracted into a reusable function. The "pending" counter pattern for tracking async completion is repeated in the report endpoint (lines 87, 93, 97, 118, 121).
Impact: Any change to error handling format requires updating every route handler. Inconsistent error responses may confuse API consumers.
Recommendation: Create a centralized error handler middleware and a reusable async wrapper. Extract the audit logging into a service method. Use Promises or async/await instead of manual callback counting.

### [MEDIUM] Inconsistent Error Handling
File: src/AppManager.js:35, 38, 41, 48, 51, 54, 57, 70, 84, 135
Description: Error responses mix plain text strings (`res.status(400).send("Bad Request")`, `res.status(500).send("Erro DB")`) and JSON objects (`res.status(200).json({...})`). There is no standardized error response format. Internal error details are leaked to the client (e.g., "Erro DB", "Erro Matrícula", "Erro Pagamento").
Impact: API consumers cannot reliably parse error responses. Internal implementation details are exposed, potentially aiding attackers. Error handling is inconsistent across endpoints.
Recommendation: Implement a centralized error handler middleware that always returns JSON responses in a consistent format. Use custom error classes for different error types. Never expose internal error messages to the client.

### [MEDIUM] Data Integrity Issue — Orphaned Records
File: src/AppManager.js:131-137
Description: The user deletion endpoint deletes a user but explicitly acknowledges that enrollments and payments become orphaned: `"Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco."`. There are no foreign key constraints with CASCADE DELETE defined in the schema (lines 12-16).
Impact: Database integrity degrades over time as deleted users leave orphaned enrollments and payments. This can cause incorrect financial reports, broken referential integrity, and wasted storage.
Recommendation: Either enable foreign keys in SQLite (`PRAGMA foreign_keys = ON`) and add ON DELETE CASCADE to the schema, or perform cascading deletes manually in the route handler. Add a cleanup migration to remove existing orphaned records.

### [LOW] Magic Numbers
File: src/utils.js:19, 22
Description: The numbers `10000` (loop iterations) and `10` (string truncation length) in `badCrypto` are magic numbers with no named constant or explanation. These values control the "strength" of the custom hashing algorithm.
Impact: The purpose and effect of these values is unclear to maintainers. Changing them could silently weaken or break the password hashing behavior.
Recommendation: Replace with named constants (`const HASH_ITERATIONS = 10000; const HASH_TRUNCATE_LENGTH = 10;`). Better yet, remove the custom function entirely and use bcryptjs (already in dependencies).

### [LOW] Inconsistent Naming
File: src/AppManager.js:28-34, 80-81, 131-132
Description: Variable names are abbreviated inconsistently: `u` (user name), `e` (email), `p` (password), `cid` (course ID), `cc` (credit card), `enr` (enrollment). The endpoint path uses snake_case (`/api/admin/financial-report`) while the API generally uses kebab-case. The `badCrypto` function name is informal and ambiguous.
Impact: Reduces code readability and makes the codebase harder to understand for new developers. Abbreviated names obscure the intent of variables.
Recommendation: Use descriptive, full-word variable names throughout. Follow a consistent naming convention (camelCase for JavaScript). Rename `badCrypto` to `hashPassword` or `encryptPassword` (or replace with bcryptjs).

---
Total: 11 findings

---
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]