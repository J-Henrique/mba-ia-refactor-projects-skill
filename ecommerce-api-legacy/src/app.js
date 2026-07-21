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

// Middleware de erro centralizado
app.use((err, _req, res, _next) => {
  console.error('[ERROR]', err.stack || err.message || err);
  res.status(500).json({ error: 'Erro interno do servidor' });
});

app.listen(config.port, () => {
  console.log(`ecommerce-api-legacy rodando na porta ${config.port}...`);
});