const express = require('express');

const CheckoutController = require('../controllers/CheckoutController');
const ReportController = require('../controllers/ReportController');
const UserController = require('../controllers/UserController');

function createRouter(db) {
    const router = express.Router();

    const checkoutController = new CheckoutController(db);
    const reportController = new ReportController(db);
    const userController = new UserController(db);

    // Checkout
    router.post('/api/checkout', (req, res) => checkoutController.checkout(req, res));

    // Financial report
    router.get('/api/admin/financial-report', (req, res) =>
        reportController.financialReport(req, res)
    );

    // User deletion
    router.delete('/api/users/:id', (req, res) => userController.deleteUser(req, res));

    return router;
}

module.exports = createRouter;