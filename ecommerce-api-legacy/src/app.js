const express = require('express');
const config = require('./config/config');
const Database = require('./models/Database');
const UserModel = require('./models/UserModel');
const CourseModel = require('./models/CourseModel');
const EnrollmentModel = require('./models/EnrollmentModel');
const PaymentModel = require('./models/PaymentModel');
const AuditLogModel = require('./models/AuditLogModel');
const CheckoutController = require('./controllers/CheckoutController');
const ReportController = require('./controllers/ReportController');
const UserController = require('./controllers/UserController');
const createRoutes = require('./routes/index');
const { errorHandler } = require('./middlewares/errorHandler');

const app = express();
app.use(express.json());

const db = new Database();
const userModel = new UserModel(db);
const courseModel = new CourseModel(db);
const enrollmentModel = new EnrollmentModel(db);
const paymentModel = new PaymentModel(db);
const auditLogModel = new AuditLogModel(db);

const checkoutController = new CheckoutController(userModel, courseModel, enrollmentModel, paymentModel, auditLogModel);
const reportController = new ReportController(courseModel, enrollmentModel);
const userController = new UserController(userModel);

app.use(createRoutes(checkoutController, reportController, userController));
app.use(errorHandler);

db.init()
    .then(() => {
        app.listen(config.port, () => {
            console.log(`LMS rodando na porta ${config.port}...`);
        });
    })
    .catch((err) => {
        console.error('Erro ao inicializar banco:', err);
        process.exit(1);
    });

module.exports = app;