const { AppError } = require('../middlewares/errorHandler');

class UserController {
    constructor(userModel) {
        this.userModel = userModel;
    }

    async delete(req, res, next) {
        try {
            const { id } = req.params;
            await this.userModel.delete(id);
            return res.send('Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.');
        } catch (err) {
            next(err);
        }
    }
}

module.exports = UserController;