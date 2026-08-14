const { Router } = require('express');

function createRoutes(checkoutController, reportController, userController) {
    const router = new Router();

    router.post('/api/checkout', (req, res, next) => checkoutController.checkout(req, res, next));
    router.get('/api/admin/financial-report', (req, res, next) => reportController.financialReport(req, res, next));
    router.delete('/api/users/:id', (req, res, next) => userController.delete(req, res, next));

    return router;
}

module.exports = createRoutes;