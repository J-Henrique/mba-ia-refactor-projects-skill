class PaymentModel {
    constructor(db) {
        this.db = db;
    }

    async create(enrollmentId, amount, status) {
        const result = await this.db.run(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollmentId, amount, status]
        );
        return result.lastID;
    }

    async findByEnrollmentId(enrollmentId) {
        return this.db.get("SELECT amount, status FROM payments WHERE enrollment_id = ?", [enrollmentId]);
    }
}

module.exports = PaymentModel;