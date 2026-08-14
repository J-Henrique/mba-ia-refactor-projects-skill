require('dotenv').config();

const config = {
    port: parseInt(process.env.PORT, 10) || 3000,
    dbUser: process.env.DB_USER,
    dbPass: process.env.DB_PASS,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    smtpUser: process.env.SMTP_USER,
    bcryptSaltRounds: 10,
};

module.exports = config;