import logging
from flask import request, jsonify
import models

logger = logging.getLogger(__name__)

# Constantes de validacao
NOME_MIN_LEN = 2
NOME_MAX_LEN = 200
CATEGORIAS_VALIDAS = [
    "informatica", "moveis", "vestuario", "geral", "eletronicos", "livros",
]


def listar_produtos():
    try:
        produtos = models.get_todos_produtos()
        logger.info("Listando %d produtos", len(produtos))
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception as e:
        logger.error("Erro ao listar produtos: %s", str(e))
        return jsonify({"erro": str(e)}), 500


def buscar_produto(id):
    try:
        produto = models.get_produto_por_id(id)
        if produto:
            return jsonify({"dados": produto, "sucesso": True}), 200
        return jsonify({"erro": "Produto nao encontrado", "sucesso": False}), 404
    except Exception as e:
        logger.error("Erro ao buscar produto %d: %s", id, str(e))
        return jsonify({"erro": str(e)}), 500


def criar_produto():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Dados invalidos"}), 400
        if "nome" not in dados:
            return jsonify({"erro": "Nome e obrigatorio"}), 400
        if "preco" not in dados:
            return jsonify({"erro": "Preco e obrigatorio"}), 400
        if "estoque" not in dados:
            return jsonify({"erro": "Estoque e obrigatorio"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return jsonify({"erro": "Preco nao pode ser negativo"}), 400
        if estoque < 0:
            return jsonify({"erro": "Estoque nao pode ser negativo"}), 400
        if len(nome) < NOME_MIN_LEN:
            return jsonify({"erro": "Nome muito curto"}), 400
        if len(nome) > NOME_MAX_LEN:
            return jsonify({"erro": "Nome muito longo"}), 400
        if categoria not in CATEGORIAS_VALIDAS:
            return jsonify(
                {"erro": "Categoria invalida. Validas: " + str(CATEGORIAS_VALIDAS)}
            ), 400

        id = models.criar_produto(nome, descricao, preco, estoque, categoria)
        logger.info("Produto criado com ID: %d", id)
        return jsonify(
            {"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}
        ), 201

    except Exception as e:
        logger.error("Erro ao criar produto: %s", str(e))
        return jsonify({"erro": str(e)}), 500


def atualizar_produto(id):
    try:
        dados = request.get_json()

        produto_existente = models.get_produto_por_id(id)
        if not produto_existente:
            return jsonify({"erro": "Produto nao encontrado"}), 404

        if not dados:
            return jsonify({"erro": "Dados invalidos"}), 400
        if "nome" not in dados:
            return jsonify({"erro": "Nome e obrigatorio"}), 400
        if "preco" not in dados:
            return jsonify({"erro": "Preco e obrigatorio"}), 400
        if "estoque" not in dados:
            return jsonify({"erro": "Estoque e obrigatorio"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return jsonify({"erro": "Preco nao pode ser negativo"}), 400
        if estoque < 0:
            return jsonify({"erro": "Estoque nao pode ser negativo"}), 400

        models.atualizar_produto(id, nome, descricao, preco, estoque, categoria)
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

    except Exception as e:
        logger.error("Erro ao atualizar produto %d: %s", id, str(e))
        return jsonify({"erro": str(e)}), 500


def deletar_produto(id):
    try:
        produto = models.get_produto_por_id(id)
        if not produto:
            return jsonify({"erro": "Produto nao encontrado"}), 404

        models.deletar_produto(id)
        logger.info("Produto %d deletado", id)
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
    except Exception as e:
        logger.error("Erro ao deletar produto %d: %s", id, str(e))
        return jsonify({"erro": str(e)}), 500


def buscar_produtos():
    try:
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = request.args.get("preco_min", None)
        preco_max = request.args.get("preco_max", None)

        if preco_min:
            preco_min = float(preco_min)
        if preco_max:
            preco_max = float(preco_max)

        resultados = models.buscar_produtos(termo, categoria, preco_min, preco_max)
        return jsonify(
            {"dados": resultados, "total": len(resultados), "sucesso": True}
        ), 200
    except Exception as e:
        logger.error("Erro ao buscar produtos: %s", str(e))
        return jsonify({"erro": str(e)}), 500