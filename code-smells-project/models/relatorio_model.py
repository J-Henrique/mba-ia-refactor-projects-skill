from database import get_db

# Limiares para cálculo de desconto progressivo
DESCONTO_10_PERCENT_LIMITE = 10000
DESCONTO_5_PERCENT_LIMITE = 5000
DESCONTO_2_PERCENT_LIMITE = 1000

DESCONTO_10_PERCENT = 0.10
DESCONTO_5_PERCENT = 0.05
DESCONTO_2_PERCENT = 0.02


def relatorio_vendas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*), SUM(total) FROM pedidos")
    total_pedidos, faturamento = cursor.fetchone()
    faturamento = faturamento or 0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]

    desconto = 0
    if faturamento > DESCONTO_10_PERCENT_LIMITE:
        desconto = faturamento * DESCONTO_10_PERCENT
    elif faturamento > DESCONTO_5_PERCENT_LIMITE:
        desconto = faturamento * DESCONTO_5_PERCENT
    elif faturamento > DESCONTO_2_PERCENT_LIMITE:
        desconto = faturamento * DESCONTO_2_PERCENT

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": (
            round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0
        ),
    }