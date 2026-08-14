class AppError extends Error {
    constructor(message, statusCode = 400) {
        super(message);
        this.statusCode = statusCode;
    }
}

function errorHandler(err, req, res, next) {
    if (err instanceof AppError) {
        return res.status(err.statusCode).json({ error: err.message });
    }

    console.error(`[ERROR] ${err.message}`, err.stack);
    return res.status(500).json({ error: 'Erro interno do servidor' });
}

module.exports = { AppError, errorHandler };