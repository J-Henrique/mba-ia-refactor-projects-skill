from flask import request, jsonify
import models.models as models

def listar_produtos():
    try:
        produtos = models.get_todos_produtos()
        print("Listando " + str(len(produtos)) + " produtos")
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception as e:
        print("ERRO: " + str(e))
        return jsonify({"erro": str(e)}), 500

def buscar_produto(id):
    try:
        produto = models.get_produto_por_id(id)
        if produto:
            return jsonify({"dados": produto, "sucesso": True}), 200
        else:
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def criar_produto():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        if "nome" not in dados:
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if "preco" not in dados:
            return jsonify({"erro": "Preço é obrigatório"}), 400
        if "estoque" not in dados:
            return jsonify({"erro": "Estoque é obrigatório"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return jsonify({"erro": "Preço não pode ser negativo"}), 400
        if estoque < 0:
            return jsonify({"erro": "Estoque não pode ser negativo"}), 400
        if len(nome) < 2:
            return jsonify({"erro": "Nome muito curto"}), 400
        if len(nome) > 200:
            return jsonify({"erro": "Nome muito longo"}), 400

        categorias_validas = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
        if categoria not in categorias_validas:
            return jsonify({"erro": "Categoria inválida. Válidas: " + str(categorias_validas)}), 400

        id = models.criar_produto(nome, descricao, preco, estoque, categoria)
        print("Produto criado com ID: " + str(id))
        return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201

    except Exception as e:
        print("ERRO ao criar produto: " + str(e))
        return jsonify({"erro": str(e)}), 500

def atualizar_produto(id):
    try:
        dados = request.get_json()

        produto_existente = models.get_produto_por_id(id)
        if not produto_existente:
            return jsonify({"erro": "Produto não encontrado"}), 404

        if not dados:
            return jsonify({"erro": "Dados inválidos"}), 400
        if "nome" not in dados:
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if "preco" not in dados:
            return jsonify({"erro": "Preço é obrigatório"}), 400
        if "estoque" not in dados:
            return jsonify({"erro": "Estoque é obrigatório"}), 400

        nome = dados["nome"]
        descricao = dados.get("descricao", "")
        preco = dados["preco"]
        estoque = dados["estoque"]
        categoria = dados.get("categoria", "geral")

        if preco < 0:
            return jsonify({"erro": "Preço não pode ser negativo"}), 400
        if estoque < 0:
            return jsonify({"erro": "Estoque não pode ser negativo"}), 400

        models.atualizar_produto(id, nome, descricao, preco, estoque, categoria)
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def deletar_produto(id):
    try:

        produto = models.get_produto_por_id(id)
        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404

        models.deletar_produto(id)
        print("Produto " + str(id) + " deletado")
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
    except Exception as e:
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
        return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
