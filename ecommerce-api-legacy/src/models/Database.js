const sqlite3 = require('sqlite3').verbose();

class Database {
    constructor(dbPath = ':memory:') {
        this.db = new sqlite3.Database(dbPath);
    }

    init() {
        this.db.serialize(() => {
            // Enable foreign keys for cascade deletes
            this.db.run("PRAGMA foreign_keys = ON");

            this.db.run(
                "CREATE TABLE IF NOT EXISTS users (" +
                "id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)"
            );
            this.db.run(
                "CREATE TABLE IF NOT EXISTS courses (" +
                "id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)"
            );
            this.db.run(
                "CREATE TABLE IF NOT EXISTS enrollments (" +
                "id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER, " +
                "FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, " +
                "FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE)"
            );
            this.db.run(
                "CREATE TABLE IF NOT EXISTS payments (" +
                "id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT, " +
                "FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE)"
            );
            this.db.run(
                "CREATE TABLE IF NOT EXISTS audit_logs (" +
                "id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)"
            );

            // Seed data
            this.db.run(
                "INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', '123')"
            );
            this.db.run(
                "INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1), ('Docker', 497.00, 1)"
            );
            this.db.run("INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)");
            this.db.run(
                "INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')"
            );
        });
    }

    // --- User queries ---
    getUserByEmail(email) {
        return new Promise((resolve, reject) => {
            this.db.get("SELECT id FROM users WHERE email = ?", [email], (err, row) => {
                if (err) return reject(err);
                resolve(row);
            });
        });
    }

    createUser(name, email, pass) {
        return new Promise((resolve, reject) => {
            this.db.run(
                "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
                [name, email, pass],
                function (err) {
                    if (err) return reject(err);
                    resolve(this.lastID);
                }
            );
        });
    }

    deleteUser(userId) {
        return new Promise((resolve, reject) => {
            this.db.run("DELETE FROM users WHERE id = ?", [userId], function (err) {
                if (err) return reject(err);
                resolve(this.changes);
            });
        });
    }

    // --- Course queries ---
    getActiveCourse(courseId) {
        return new Promise((resolve, reject) => {
            this.db.get(
                "SELECT * FROM courses WHERE id = ? AND active = 1",
                [courseId],
                (err, row) => {
                    if (err) return reject(err);
                    resolve(row);
                }
            );
        });
    }

    getAllCourses() {
        return new Promise((resolve, reject) => {
            this.db.all("SELECT * FROM courses", [], (err, rows) => {
                if (err) return reject(err);
                resolve(rows);
            });
        });
    }

    // --- Enrollment queries ---
    createEnrollment(userId, courseId) {
        return new Promise((resolve, reject) => {
            this.db.run(
                "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
                [userId, courseId],
                function (err) {
                    if (err) return reject(err);
                    resolve(this.lastID);
                }
            );
        });
    }

    // --- Payment queries ---
    createPayment(enrollmentId, amount, status) {
        return new Promise((resolve, reject) => {
            this.db.run(
                "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
                [enrollmentId, amount, status],
                function (err) {
                    if (err) return reject(err);
                    resolve(this.lastID);
                }
            );
        });
    }

    // --- Audit log queries ---
    createAuditLog(action) {
        return new Promise((resolve, reject) => {
            this.db.run(
                "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
                [action],
                function (err) {
                    if (err) return reject(err);
                    resolve(this.lastID);
                }
            );
        });
    }

    // --- Financial report (uses JOIN to eliminate N+1) ---
    getFinancialReport() {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT
                    c.id AS course_id,
                    c.title AS course_title,
                    c.price AS course_price,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    e.id AS enrollment_id,
                    p.id AS payment_id,
                    p.amount AS payment_amount,
                    p.status AS payment_status
                FROM courses c
                LEFT JOIN enrollments e ON e.course_id = c.id
                LEFT JOIN users u ON u.id = e.user_id
                LEFT JOIN payments p ON p.enrollment_id = e.id
                ORDER BY c.id, e.id
            `;
            this.db.all(query, [], (err, rows) => {
                if (err) return reject(err);
                resolve(rows);
            });
        });
    }
}

module.exports = Database;