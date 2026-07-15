from flask import Blueprint, jsonify, request
import controllers

api_blueprint = Blueprint('api', __name__)

# Produtos
api_blueprint.add_url_rule("/produtos", "listar_produtos", controllers.listar_produtos, methods=["GET"])
api_blueprint.add_url_rule("/produtos/busca", "buscar_produtos", controllers.buscar_produtos, methods=["GET"])
api_blueprint.add_url_rule("/produtos/<int:id>", "buscar_produto", controllers.buscar_produto, methods=["GET"])
api_blueprint.add_url_rule("/produtos", "criar_produto", controllers.criar_produto, methods=["POST"])
api_blueprint.add_url_rule("/produtos/<int:id>", "atualizar_produto", controllers.atualizar_produto, methods=["PUT"])
api_blueprint.add_url_rule("/produtos/<int:id>", "deletar_produto", controllers.deletar_produto, methods=["DELETE"])

# Usuários
api_blueprint.add_url_rule("/usuarios", "listar_usuarios", controllers.listar_usuarios, methods=["GET"])
api_blueprint.add_url_rule("/usuarios/<int:id>", "buscar_usuario", controllers.buscar_usuario, methods=["GET"])
api_blueprint.add_url_rule("/usuarios", "criar_usuario", controllers.criar_usuario, methods=["POST"])
api_blueprint.add_url_rule("/login", "login", controllers.login, methods=["POST"])

# Pedidos
api_blueprint.add_url_rule("/pedidos", "criar_pedido", controllers.criar_pedido, methods=["POST"])
api_blueprint.add_url_rule("/pedidos", "listar_todos_pedidos", controllers.listar_todos_pedidos, methods=["GET"])
api_blueprint.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", controllers.listar_pedidos_usuario, methods=["GET"])
api_blueprint.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", controllers.atualizar_status_pedido, methods=["PUT"])

# Relatórios
api_blueprint.add_url_rule("/relatorios/vendas", "relatorio_vendas", controllers.relatorio_vendas, methods=["GET"])

# Health
api_blueprint.add_url_rule("/health", "health_check", controllers.health_check, methods=["GET"])
