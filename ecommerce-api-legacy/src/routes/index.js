/** Route definitions for ecommerce-api-legacy. */

const { Router } = require("express");
const CheckoutController = require("../controllers/CheckoutController");
const ReportController = require("../controllers/ReportController");
const UserController = require("../controllers/UserController");

const router = Router();

// Checkout
router.post("/api/checkout", CheckoutController.checkout);

// Reports
router.get("/api/admin/financial-report", ReportController.financialReport);

// Users
router.delete("/api/users/:id", UserController.deleteUser);

module.exports = router;