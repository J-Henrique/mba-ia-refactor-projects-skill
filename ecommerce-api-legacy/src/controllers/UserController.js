class UserController {
    constructor(db) {
        this.db = db;
    }

    async deleteUser(req, res) {
        try {
            const userId = req.params.id;
            const changes = await this.db.deleteUser(userId);

            if (changes === 0) {
                return res.status(404).json({ error: 'Usuário não encontrado' });
            }

            // Foreign keys with CASCADE DELETE handle enrollments and payments
            return res.json({ message: 'Usuário deletado com sucesso' });
        } catch (err) {
            return res.status(500).json({ error: err.message });
        }
    }
}

module.exports = UserController;