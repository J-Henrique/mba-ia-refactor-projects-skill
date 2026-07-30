class ReportController {
    constructor(db) {
        this.db = db;
    }

    async financialReport(req, res) {
        try {
            const rows = await this.db.getFinancialReport();

            // Group rows into structured report
            const courseMap = {};

            for (const row of rows) {
                if (!courseMap[row.course_id]) {
                    courseMap[row.course_id] = {
                        course: row.course_title,
                        revenue: 0,
                        students: [],
                    };
                }

                if (row.user_id) {
                    const amount = row.payment_amount || 0;
                    if (row.payment_status === 'PAID') {
                        courseMap[row.course_id].revenue += amount;
                    }
                    courseMap[row.course_id].students.push({
                        student: row.user_name || 'Unknown',
                        paid: amount,
                    });
                }
            }

            const report = Object.values(courseMap);
            return res.json(report);
        } catch (err) {
            return res.status(500).json({ error: err.message });
        }
    }
}

module.exports = ReportController;