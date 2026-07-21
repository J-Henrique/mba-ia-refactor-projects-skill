const db = require('../models/Database');

class ReportController {
  static async financialReport(req, res) {
    try {
      const rows = await new Promise((resolve, reject) => {
        db.all(
          `SELECT
            c.id AS course_id,
            c.title AS course_title,
            u.name AS student_name,
            u.email AS student_email,
            p.amount AS payment_amount,
            p.status AS payment_status
          FROM courses c
          LEFT JOIN enrollments e ON c.id = e.course_id
          LEFT JOIN users u ON e.user_id = u.id
          LEFT JOIN payments p ON e.id = p.enrollment_id
          ORDER BY c.id`,
          [],
          (err, rows) => err ? reject(err) : resolve(rows)
        );
      });

      const courseMap = {};
      const report = [];

      for (const row of rows) {
        if (!courseMap[row.course_id]) {
          courseMap[row.course_id] = {
            course: row.course_title,
            revenue: 0,
            students: [],
          };
          report.push(courseMap[row.course_id]);
        }

        if (row.student_name) {
          const paid = row.payment_status === 'PAID' ? row.payment_amount : 0;
          courseMap[row.course_id].students.push({
            student: row.student_name,
            paid,
          });
          if (row.payment_status === 'PAID') {
            courseMap[row.course_id].revenue += row.payment_amount;
          }
        }
      }

      res.json(report);
    } catch (err) {
      console.error(err);
      res.status(500).send("Erro ao gerar relatório");
    }
  }
}

module.exports = ReportController;