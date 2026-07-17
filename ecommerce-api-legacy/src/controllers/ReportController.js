const db = require('../models/Database');

class ReportController {
    static async financialReport(req, res) {
        try {
            const courses = await new Promise((resolve, reject) => {
                db.all("SELECT * FROM courses", [], (err, rows) => err ? reject(err) : resolve(rows));
            });

            const report = await Promise.all(courses.map(async (c) => {
                const enrollments = await new Promise((resolve, reject) => {
                    db.all("SELECT * FROM enrollments WHERE course_id = ?", [c.id], (err, rows) => err ? reject(err) : resolve(rows));
                });

                const students = await Promise.all(enrollments.map(async (enr) => {
                    const user = await new Promise((resolve, reject) => {
                        db.get("SELECT name, email FROM users WHERE id = ?", [enr.user_id], (err, row) => err ? reject(err) : resolve(row));
                    });
                    const payment = await new Promise((resolve, reject) => {
                        db.get("SELECT amount, status FROM payments WHERE enrollment_id = ?", [enr.id], (err, row) => err ? reject(err) : resolve(row));
                    });
                    return {
                        student: user ? user.name : 'Unknown',
                        paid: (payment && payment.status === 'PAID') ? payment.amount : 0
                    };
                }));

                const revenue = students.reduce((sum, s) => sum + s.paid, 0);

                return { course: c.title, revenue, students };
            }));

            res.json(report);
        } catch (err) {
            console.error(err);
            res.status(500).send("Erro ao gerar relatório");
        }
    }
}

module.exports = ReportController;
