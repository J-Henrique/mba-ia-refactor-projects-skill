const express = require('express');
const Database = require('./models/Database');
const createRouter = require('./routes/index');
const errorHandler = require('./middlewares/errorHandler');
const { config } = require('./config/config');

const app = express();
app.use(express.json());

const db = new Database();
db.init();

app.use(createRouter(db));

// Centralized error handler
app.use(errorHandler);

app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
});