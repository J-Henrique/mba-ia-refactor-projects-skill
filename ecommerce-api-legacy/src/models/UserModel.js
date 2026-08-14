class UserModel {
    constructor(db) {
        this.db = db;
    }

    async findByEmail(email) {
        return this.db.get("SELECT id, name, email, pass FROM users WHERE email = ?", [email]);
    }

    async findById(id) {
        return this.db.get("SELECT id, name, email FROM users WHERE id = ?", [id]);
    }

    async create(name, email, passwordHash) {
        const result = await this.db.run(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, passwordHash]
        );
        return result.lastID;
    }

    async delete(id) {
        return this.db.run("DELETE FROM users WHERE id = ?", [id]);
    }
}

module.exports = UserModel;