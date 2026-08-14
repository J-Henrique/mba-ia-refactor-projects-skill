const { AppError } = require('../middlewares/errorHandler');

class ReportController {
    constructor(courseModel, enrollmentModel) {
        this.courseModel = courseModel;
        this.enrollmentModel = enrollmentModel;
    }

    async financialReport(req, res, next) {
        try {
            const courses = await this.courseModel.findAll();
            const report = [];

            for (const course of courses) {
                const enrollments = await this.enrollmentModel.findWithUsersAndPaymentsByCourseId(course.id);
                const courseData = { course: course.title, revenue: 0, students: [] };

                for (const enr of enrollments) {
                    if (enr.payment_status === 'PAID') {
                        courseData.revenue += enr.payment_amount || 0;
                    }
                    courseData.students.push({
                        student: enr.user_name || 'Unknown',
                        paid: enr.payment_amount || 0,
                    });
                }

                report.push(courseData);
            }

            return res.json(report);
        } catch (err) {
            next(err);
        }
    }
}

module.exports = ReportController;