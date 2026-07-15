from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import Config
from routes.routes import api_blueprint
from database import get_db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Registrar rotas
app.register_blueprint(api_blueprint)

@app.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0"
    })

if __name__ == "__main__":
    get_db()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
