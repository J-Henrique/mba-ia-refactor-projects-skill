const express = require("express");
const config = require("./config/config");
const routes = require("./routes");

const app = express();
app.use(express.json());

// Routes
app.use(routes);

// Centralized error middleware
app.use((err, _req, res, _next) => {
  console.error("[ERROR]", err.stack || err.message || err);
  res.status(500).json({ error: "Erro interno do servidor" });
});

app.listen(config.port, () => {
  console.log(`ecommerce-api-legacy rodando na porta ${config.port}...`);
});