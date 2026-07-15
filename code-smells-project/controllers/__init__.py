from .produto_controller import *
from .usuario_controller import *
from .pedido_controller import *
from .relatorio_controller import *

# Funções utilitárias que não pertencem a um controller específico
from flask import jsonify

def health_check():
    try:
        from database import get_db
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos = cursor.fetchone()[0]

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": produtos,
                "usuarios": usuarios,
                "pedidos": pedidos
            },
            "versao": "1.0.0",
            "ambiente": "producao",
            "db_path": "loja.db",
            "debug": True
        }), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500
