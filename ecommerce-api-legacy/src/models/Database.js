const sqlite3 = require('sqlite3').verbose();
const { promisify } = require('util');

class Database {
    constructor(dbPath = ':memory:') {
        this.db = new sqlite3.Database(dbPath);
        this.get = promisify(this.db.get.bind(this.db));
        this.all = promisify(this.db.all.bind(this.db));
    }

    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) return reject(err);
                resolve({ lastID: this.lastID, changes: this.changes });
            });
        });
    }

    async init() {
        await this.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)");
        await this.run("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)");
        await this.run("CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)");
        await this.run("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)");
        await this.run("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)");

        await this.run("INSERT OR IGNORE INTO users (id, name, email, pass) VALUES (1, 'Leonan', 'leonan@fullcycle.com.br', '123')");
        await this.run("INSERT OR IGNORE INTO courses (id, title, price, active) VALUES (1, 'Clean Architecture', 997.00, 1), (2, 'Docker', 497.00, 1)");
        await this.run("INSERT OR IGNORE INTO enrollments (id, user_id, course_id) VALUES (1, 1, 1)");
        await this.run("INSERT OR IGNORE INTO payments (id, enrollment_id, amount, status) VALUES (1, 1, 997.00, 'PAID')");
    }
}

module.exports = Database;