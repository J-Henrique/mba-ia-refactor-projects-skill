const db = require('../models/Database');
const { hashPassword } = require('../utils/security');
const { config } = require('../config/config');

class CheckoutController {
    static async checkout(req, res) {
        const { usr, eml, pwd, c_id, card } = req.body;
        if (!usr || !eml || !c_id || !card) return res.status(400).send("Bad Request");

        try {
            const course = await new Promise((resolve, reject) => {
                db.get("SELECT * FROM courses WHERE id = ? AND active = 1", [c_id], (err, row) => err ? reject(err) : resolve(row));
            });
            if (!course) return res.status(404).send("Curso não encontrado");

            let user = await new Promise((resolve, reject) => {
                db.get("SELECT id FROM users WHERE email = ?", [eml], (err, row) => err ? reject(err) : resolve(row));
            });

            if (!user) {
                const hash = hashPassword(pwd || "123456");
                user = await new Promise((resolve, reject) => {
                    db.run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)", [usr, eml, hash], function(err) {
                        err ? reject(err) : resolve({ id: this.lastID });
                    });
                });
            }

            const status = card.startsWith("4") ? "PAID" : "DENIED";
            if (status === "DENIED") return res.status(400).send("Pagamento recusado");

            const enrId = await new Promise((resolve, reject) => {
                db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [user.id, c_id], function(err) {
                    err ? reject(err) : resolve(this.lastID);
                });
            });

            await new Promise((resolve, reject) => {
                db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [enrId, course.price, status], (err) => err ? reject(err) : resolve());
            });

            await new Promise((resolve, reject) => {
                db.run("INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))", [`Checkout curso ${c_id} por ${user.id}`], (err) => err ? reject(err) : resolve());
            });

            res.status(200).json({ msg: "Sucesso", enrollment_id: enrId });
        } catch (err) {
            console.error(err);
            res.status(500).send("Erro interno");
        }
    }
}

module.exports = CheckoutController;
