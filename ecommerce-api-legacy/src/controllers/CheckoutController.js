const config = require('../config/config');
const { hashPassword } = require('../utils/security');
const { AppError } = require('../middlewares/errorHandler');

class CheckoutController {
    constructor(userModel, courseModel, enrollmentModel, paymentModel, auditLogModel) {
        this.userModel = userModel;
        this.courseModel = courseModel;
        this.enrollmentModel = enrollmentModel;
        this.paymentModel = paymentModel;
        this.auditLogModel = auditLogModel;
    }

    async checkout(req, res, next) {
        try {
            const { usr: userName, eml: email, pwd: password, c_id: courseId, card: cardNumber } = req.body;

            if (!userName || !email || !courseId || !cardNumber) {
                throw new AppError('Bad Request', 400);
            }

            const course = await this.courseModel.findActiveById(courseId);
            if (!course) {
                throw new AppError('Curso não encontrado', 404);
            }

            let user = await this.userModel.findByEmail(email);

            let userId;
            if (!user) {
                const hash = hashPassword(password || '123456');
                userId = await this.userModel.create(userName, email, hash);
            } else {
                userId = user.id;
            }

            const status = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
            if (status === 'DENIED') {
                throw new AppError('Pagamento recusado', 400);
            }

            const enrollmentId = await this.enrollmentModel.create(userId, courseId);
            await this.paymentModel.create(enrollmentId, course.price, status);
            await this.auditLogModel.log(`Checkout curso ${courseId} por ${userId}`);

            return res.status(200).json({ msg: 'Sucesso', enrollment_id: enrollmentId });
        } catch (err) {
            next(err);
        }
    }
}

module.exports = CheckoutController;