require('dotenv').config();

module.exports = {
  port: parseInt(process.env.PORT, 10) || 3000,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
  dbUser: process.env.DB_USER,
  dbPass: process.env.DB_PASS,
  smtpUser: process.env.SMTP_USER,
};