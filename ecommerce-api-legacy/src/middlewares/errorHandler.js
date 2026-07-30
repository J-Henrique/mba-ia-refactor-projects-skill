function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${err.message}`, err.stack);
    const status = err.statusCode || 500;
    res.status(status).json({
        error: err.message || 'Internal Server Error',
    });
}

module.exports = errorHandler;