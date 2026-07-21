import logging
from flask import request, jsonify
import models

logger = logging.getLogger(__name__)

STATUS_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]


def criar_pedido():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Dados invalidos"}), 400

        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])

        if not usuario_id:
            return jsonify({"erro": "Usuario ID e obrigatorio"}), 400
        if not itens or len(itens) == 0:
            return jsonify({"erro": "Pedido deve ter pelo menos 1 item"}), 400

        resultado = models.criar_pedido(usuario_id, itens)

        if "erro" in resultado:
            return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

        logger.info(
            "Pedido %d criado para usuario %d",
            resultado["pedido_id"],
            usuario_id,
        )
        return jsonify(
            {
                "dados": resultado,
                "sucesso": True,
                "mensagem": "Pedido criado com sucesso",
            }
        ), 201

    except Exception as e:
        logger.error("Erro ao criar pedido: %s", str(e))
        return jsonify({"erro": str(e)}), 500


def listar_pedidos_usuario(usuario_id):
    try:
        pedidos = models.get_pedidos_usuario(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        logger.error(
            "Erro ao listar pedidos do usuario %d: %s", usuario_id, str(e)
        )
        return jsonify({"erro": str(e)}), 500


def listar_todos_pedidos():
    try:
        pedidos = models.get_todos_pedidos()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception as e:
        logger.error("Erro ao listar todos os pedidos: %s", str(e))
        return jsonify({"erro": str(e)}), 500


def atualizar_status_pedido(pedido_id):
    try:
        dados = request.get_json()
        novo_status = dados.get("status", "")

        if novo_status not in STATUS_VALIDOS:
            return jsonify(
                {
                    "erro": "Status invalido. Validos: " + str(STATUS_VALIDOS),
                    "sucesso": False,
                }
            ), 400

        models.atualizar_status_pedido(pedido_id, novo_status)
        logger.info("Pedido %d atualizado para status: %s", pedido_id, novo_status)
        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200

    except Exception as e:
        logger.error("Erro ao atualizar status do pedido %d: %s", pedido_id, str(e))
        return jsonify({"erro": str(e)}), 500