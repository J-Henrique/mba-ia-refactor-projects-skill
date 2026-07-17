# task-manager-api

API de Task Manager (Python/Flask) com organização parcial.

## Análise Manual de Problemas

Identificamos os seguintes problemas de arquitetura e qualidade no projeto, classificados por severidade:

- **CRITICAL:**
    - `app.py`: `SECRET_KEY` hardcoded ('super-secret-key-123').
    - `app.py`: `debug=True` ativado em ambiente de produção (potencialmente).
- **HIGH:**
    - `routes/task_routes.py`: "Fat Routes" - muita lógica de negócio, validação e transformação de dados misturada nas rotas.
- **MEDIUM:**
    - `routes/task_routes.py`: N+1 Queries: carregamento de `user_name` e `category_name` em loop dentro de `get_tasks`.
    - `routes/task_routes.py`: Falta de logging estruturado (uso excessivo de `print`).
    - `routes/task_routes.py`: Tratamento de erros genérico sem detalhamento.
- **LOW:**
    - `routes/task_routes.py`: Validações repetitivas espalhadas pelos métodos de rotas.
