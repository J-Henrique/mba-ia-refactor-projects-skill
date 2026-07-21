const db = require('../models/Database');
const { hashPassword } = require('../utils/security');

class CheckoutController {
  static async checkout(req, res) {
    const { usr: userName, eml: email, pwd: password, c_id: courseId, card: cardNumber } = req.body;

    if (!userName || !email || !courseId || !cardNumber) {
      return res.status(400).send("Bad Request");
    }

    try {
      const course = await new Promise((resolve, reject) => {
        db.get(
          "SELECT id, price FROM courses WHERE id = ? AND active = 1",
          [courseId],
          (err, row) => err ? reject(err) : resolve(row)
        );
      });

      if (!course) return res.status(404).send("Curso não encontrado");

      let user = await new Promise((resolve, reject) => {
        db.get(
          "SELECT id FROM users WHERE email = ?",
          [email],
          (err, row) => err ? reject(err) : resolve(row)
        );
      });

      if (!user) {
        const hashedPassword = await hashPassword(password || "123456");
        user = await new Promise((resolve, reject) => {
          db.run(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [userName, email, hashedPassword],
            function (err) {
              err ? reject(err) : resolve({ id: this.lastID });
            }
          );
        });
      }

      const paymentStatus = cardNumber.startsWith("4") ? "PAID" : "DENIED";
      if (paymentStatus === "DENIED") {
        return res.status(400).send("Pagamento recusado");
      }

      const enrollmentId = await new Promise((resolve, reject) => {
        db.run(
          "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
          [user.id, courseId],
          function (err) {
            err ? reject(err) : resolve(this.lastID);
          }
        );
      });

      await new Promise((resolve, reject) => {
        db.run(
          "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
          [enrollmentId, course.price, paymentStatus],
          (err) => err ? reject(err) : resolve()
        );
      });

      await new Promise((resolve, reject) => {
        db.run(
          "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
          [`Checkout curso ${courseId} por ${user.id}`],
          (err) => err ? reject(err) : resolve()
        );
      });

      res.status(200).json({ msg: "Sucesso", enrollment_id: enrollmentId });
    } catch (err) {
      console.error(err);
      res.status(500).send("Erro interno");
    }
  }
}

module.exports = CheckoutController;