const { hashPassword } = require('../utils/security');

class CheckoutController {
    constructor(db) {
        this.db = db;
    }

    async checkout(req, res) {
        try {
            const { usr: name, eml: email, pwd: password, c_id: courseId, card } = req.body;

            if (!name || !email || !courseId || !card) {
                return res.status(400).json({ error: 'Bad Request' });
            }

            const course = await this.db.getActiveCourse(courseId);
            if (!course) {
                return res.status(404).json({ error: 'Curso não encontrado' });
            }

            let user = await this.db.getUserByEmail(email);

            if (!user) {
                const hash = hashPassword(password || '123456');
                const userId = await this.db.createUser(name, email, hash);
                user = { id: userId };
            }

            const paymentStatus = card.startsWith('4') ? 'PAID' : 'DENIED';

            if (paymentStatus === 'DENIED') {
                return res.status(400).json({ error: 'Pagamento recusado' });
            }

            const enrollmentId = await this.db.createEnrollment(user.id, courseId);
            await this.db.createPayment(enrollmentId, course.price, paymentStatus);
            await this.db.createAuditLog(`Checkout curso ${courseId} por ${user.id}`);

            console.log(`[LOG] Salvando no cache: last_checkout_${user.id}`);
            console.log(`Processando cartão ${card} na chave ${process.env.PAYMENT_GATEWAY_KEY || 'pk_live_1234567890abcdef'}`);

            return res.status(200).json({ msg: 'Sucesso', enrollment_id: enrollmentId });
        } catch (err) {
            return res.status(500).json({ error: err.message });
        }
    }
}

module.exports = CheckoutController;