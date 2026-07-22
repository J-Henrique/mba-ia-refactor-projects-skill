# task-manager-api

API de Task Manager (Python/Flask) para gerenciamento de tarefas, usuários, categorias e relatórios. Projeto refatorado para o padrão **MVC**.

## Stack

- **Linguagem:** Python
- **Framework:** Flask
- **ORM:** Flask-SQLAlchemy
- **Banco:** SQLite
- **Hash de senha:** `werkzeug.security` (bcrypt/scrypt)

## Estrutura (MVC)

```
task-manager-api/
├── app.py                    # Entry point — inicializa app, config, blueprints, error handlers
├── config/
│   └── settings.py           # Configuração centralizada via env vars
├── controllers/              # Orquestração HTTP (ponte entre routes e services)
│   ├── task_controller.py
│   ├── user_controller.py
│   ├── report_controller.py
│   └── category_controller.py
├── models/                   # ORM (SQLAlchemy)
│   ├── task.py, user.py, category.py
├── routes/                   # Definição de endpoints (blueprints)
│   ├── task_routes.py
│   ├── user_routes.py
│   ├── report_routes.py
│   └── category_routes.py
├── services/                 # Lógica de negócio
│   ├── task_service.py
│   ├── user_service.py
│   ├── report_service.py
│   ├── category_service.py
│   └── notification_service.py
├── utils/
│   ├── helpers.py
│   └── error_handler.py      # Middleware de erro centralizado
├── database.py
├── seed.py
└── .env
```

## Funcionalidades

- **Tarefas:** CRUD completo, busca textual, estatísticas agregadas
- **Usuários:** CRUD com autenticação (login) e hash de senha seguro
- **Categorias:** CRUD completo
- **Relatórios:** Resumo geral, relatório por usuário, produtividade
- **Notificações:** Serviço de email (SMTP configurável via env vars)

## Como Rodar

```bash
pip install -r requirements.txt
cp .env.example .env  # ou configure as variáveis
python seed.py        # opcional: popula o banco com dados iniciais
python app.py
```

A aplicação sobe em `http://localhost:5000`.

## Auditoria

Relatório completo em [`reports/audit-project-3.md`](../reports/audit-project-3.md).