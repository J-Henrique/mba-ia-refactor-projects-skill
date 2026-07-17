const db = require('../models/Database');

class UserController {
    static async deleteUser(req, res) {
        const id = req.params.id;
        
        // Em um sistema real, aqui deveria ser iniciada uma transação
        try {
            await new Promise((resolve, reject) => {
                db.serialize(() => {
                    db.run("BEGIN TRANSACTION");
                    db.run("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
                    db.run("DELETE FROM enrollments WHERE user_id = ?", [id]);
                    db.run("DELETE FROM users WHERE id = ?", [id], (err) => {
                        if (err) {
                            db.run("ROLLBACK");
                            reject(err);
                        } else {
                            db.run("COMMIT");
                            resolve();
                        }
                    });
                });
            });
            res.send("Usuário e registros relacionados deletados com sucesso.");
        } catch (err) {
            console.error(err);
            res.status(500).send("Erro ao deletar usuário");
        }
    }
}

module.exports = UserController;
