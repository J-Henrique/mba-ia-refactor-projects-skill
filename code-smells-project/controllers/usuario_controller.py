from flask import request, jsonify
import models.models as models

def listar_usuarios():
    try:
        usuarios = models.get_todos_usuarios()
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def buscar_usuario(id):
    try:
        usuario = models.get_usuario_por_id(id)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True}), 200
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def criar_usuario():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400

        nome = dados.get("nome", "")
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not nome or not email or not senha:
            return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

        id = models.criar_usuario(nome, email, senha)
        return jsonify({"dados": {"id": id}, "sucesso": True}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def login():
    try:
        dados = request.get_json()
        email = dados.get("email", "")
        senha = dados.get("senha", "")

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400

        usuario = models.login_usuario(email, senha)
        if usuario:
            return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
        else:
            return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
