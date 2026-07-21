from database import get_db


def _agrupar_pedidos(rows):
    """Agrupa itens de pedido em seus respectivos pedidos (DRY helper).

    Recebe linhas de um JOIN pedidos + itens_pedido + produtos
    e retorna uma lista de dicionários com a estrutura esperada pela API.
    """
    pedidos = []
    pedido_atual = None
    for row in rows:
        pedido_id = row["id"]
        if pedido_atual is None or pedido_atual["id"] != pedido_id:
            pedido_atual = {
                "id": row["id"],
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "itens": [],
            }
            pedidos.append(pedido_atual)
        if row["item_id"] is not None:
            pedido_atual["itens"].append({
                "id": row["item_id"],
                "produto_id": row["produto_id"],
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"],
                "produto_nome": row["produto_nome"],
            })
    return pedidos


def criar_pedido(usuario_id, itens):
    db = get_db()
    cursor = db.cursor()

    # Batch-fetch todos os produtos de uma vez (evita N+1)
    produto_ids = [item["produto_id"] for item in itens]
    placeholders = ",".join("?" * len(produto_ids))
    cursor.execute(
        f"SELECT * FROM produtos WHERE id IN ({placeholders})", produto_ids
    )
    produtos = {p["id"]: dict(p) for p in cursor.fetchall()}

    total = 0
    for item in itens:
        produto = produtos.get(item["produto_id"])
        if produto is None:
            return {"erro": f"Produto {item['produto_id']} não encontrado"}
        if produto["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        total += produto["preco"] * item["quantidade"]

    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total),
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        produto = produtos[item["produto_id"]]
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
            (pedido_id, item["produto_id"], item["quantidade"], produto["preco"]),
        )
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}


def get_pedidos_usuario(usuario_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT p.*, i.id as item_id, i.produto_id, i.quantidade, i.preco_unitario,
               pr.nome as produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON i.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = i.produto_id
        WHERE p.usuario_id = ?
        ORDER BY p.id, i.id
    """,
        (usuario_id,),
    )
    return _agrupar_pedidos(cursor.fetchall())


def get_todos_pedidos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT p.*, i.id as item_id, i.produto_id, i.quantidade, i.preco_unitario,
               pr.nome as produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON i.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = i.produto_id
        ORDER BY p.id, i.id
    """
    )
    return _agrupar_pedidos(cursor.fetchall())


def atualizar_status_pedido(pedido_id, novo_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id)
    )
    db.commit()
    return True