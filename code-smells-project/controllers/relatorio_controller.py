import logging
from flask import jsonify
import models

logger = logging.getLogger(__name__)


def relatorio_vendas():
    try:
        relatorio = models.relatorio_vendas()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception as e:
        logger.error("Erro ao gerar relatorio de vendas: %s", str(e))
        return jsonify({"erro": str(e)}), 500