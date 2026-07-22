# code-smells-project

API de E-commerce desenvolvida em Python com Flask. Projeto refatorado para o padrão **MVC** (Model-View-Controller).

## Stack

- **Linguagem:** Python
- **Framework:** Flask
- **Banco:** SQLite (via sqlite3)
- **Autenticação:** `werkzeug.security` (bcrypt)

## Estrutura (MVC)

```
code-smells-project/
├── app.py                    # Entry point — inicializa app, registra blueprints, error handlers
├── config/
│   └── settings.py           # Configuração centralizada via env vars
├── controllers/              # Orquestração HTTP + validação
│   ├── produto_controller.py
│   ├── usuario_controller.py
│   ├── pedido_controller.py
│   └── relatorio_controller.py
├── models/                   # Acesso a dados (CRUD)
│   ├── produto_model.py
│   ├── usuario_model.py
│   ├── pedido_model.py
│   └── relatorio_model.py
├── routes/
│   └── routes.py             # Definição de endpoints (blueprint)
├── database.py               # Conexão SQLite + seed inicial
└── requirements.txt
```

## Funcionalidades

- **Produtos:** CRUD completo + busca com filtros (nome, categoria, preço)
- **Usuários:** CRUD + autenticação (login com hash bcrypt)
- **Pedidos:** Criação com validação de estoque, listagem por usuário, atualização de status
- **Relatórios:** Relatório de vendas agregado
- **Health Check:** Endpoint `/health` com status do banco

## Como Rodar

```bash
pip install -r requirements.txt
cp .env.example .env  # ou configure as variáveis
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot com dados de exemplo.

## Auditoria

Relatório completo em [`reports/audit-project-1.md`](../reports/audit-project-1.md).