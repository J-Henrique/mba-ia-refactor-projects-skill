class EnrollmentModel {
    constructor(db) {
        this.db = db;
    }

    async create(userId, courseId) {
        const result = await this.db.run(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        return result.lastID;
    }

    async findByCourseId(courseId) {
        return this.db.all("SELECT * FROM enrollments WHERE course_id = ?", [courseId]);
    }

    async findWithUsersAndPaymentsByCourseId(courseId) {
        return this.db.all(`
            SELECT e.id AS enrollment_id, e.user_id, e.course_id,
                   u.name AS user_name, u.email AS user_email,
                   p.amount AS payment_amount, p.status AS payment_status
            FROM enrollments e
            LEFT JOIN users u ON e.user_id = u.id
            LEFT JOIN payments p ON e.id = p.enrollment_id
            WHERE e.course_id = ?
        `, [courseId]);
    }
}

module.exports = EnrollmentModel;