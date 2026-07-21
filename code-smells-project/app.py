import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import Config
from routes.routes import api_blueprint
from database import get_db

# Configuracao centralizada de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Registrar rotas
app.register_blueprint(api_blueprint)


@app.route("/")
def index():
    return jsonify({"mensagem": "Bem-vindo a API da Loja", "versao": "1.0.0"})


# Middleware de erro global
@app.errorhandler(404)
def not_found(error):
    logger.warning("Rota nao encontrada: %s", error)
    return jsonify({"erro": "Recurso nao encontrado", "sucesso": False}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error("Erro interno do servidor: %s", error)
    return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500


@app.errorhandler(400)
def bad_request(error):
    logger.warning("Requisicao invalida: %s", error)
    return jsonify({"erro": "Requisicao invalida", "sucesso": False}), 400


if __name__ == "__main__":
    get_db()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])