const express = require('express');
const CheckoutController = require('./controllers/CheckoutController');
const ReportController = require('./controllers/ReportController');
const UserController = require('./controllers/UserController');
const config = require('./config/config');

const app = express();
app.use(express.json());

// Rotas
app.post('/api/checkout', CheckoutController.checkout);
app.get('/api/admin/financial-report', ReportController.financialReport);
app.delete('/api/users/:id', UserController.deleteUser);

app.listen(config.port, () => {
    console.log(`Frankenstein LMS refatorado rodando na porta ${config.port}...`);
});
