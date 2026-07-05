# task-manager-api

API RESTful em Python com Flask para gerenciamento de tarefas, usuários e relatórios.

## Estrutura do Projeto:

*   **`app.py`**: Ponto de entrada da aplicação Flask. Configura a aplicação, inicializa o SQLAlchemy, registra os Blueprints de rotas (`task_routes`, `user_routes`, `report_routes`) e define rotas básicas (`/health`, `/`).
*   **`database.py`**: Configura a conexão com o banco de dados SQLite (`tasks.db`) usando Flask-SQLAlchemy.
*   **`models/`**: Define os modelos de dados (ORM) com SQLAlchemy:
    *   `task.py`: Modelo para tarefas (título, descrição, status, prioridade, usuário, categoria, datas, tags).
    *   `user.py`: Modelo para usuários (nome, email, senha, papel, status).
    *   `category.py`: Modelo para categorias de tarefas (nome, descrição, cor).
*   **`routes/`**: Blueprints que definem as rotas relacionadas a cada entidade:
    *   `task_routes.py`: Operações de CRUD para tarefas, busca e estatísticas.
    *   `user_routes.py`: Rotas para usuários (registro, login, atualização, deleção).
    *   `report_routes.py`: Endpoints para relatórios de resumo, relatórios por usuário e gerenciamento de categorias.
*   **`services/`**: Contém a lógica para envio de notificações por email (simuladas).
*   **`utils/`**: Funções utilitárias genéricas.
*   **`requirements.txt`**: Lista as dependências Python (Flask, Flask-SQLAlchemy, Marshmallow, etc.).
*   **`seed.py`**: Script para popular o banco de dados com dados iniciais.

## Função da Aplicação:

A API gerencia um sistema de gerenciamento de tarefas, permitindo:

*   **Tarefas**: Criar, visualizar, atualizar, deletar, buscar e obter estatísticas sobre tarefas.
*   **Usuários**: Registrar, logar, gerenciar perfis e associar tarefas a usuários.
*   **Categorias**: Gerenciar categorias para organizar tarefas.
*   **Relatórios**: Gerar relatórios consolidados sobre tarefas, usuários e atividades.
*   **Notificações**: Simula envio de emails para notificações.

## Análise Manual de Problemas (Conforme Requisitos Mínimos do README):

*   **CRITICAL:**
    *   `models/user.py`: Uso de `hashlib.md5` para senhas, um algoritmo de hash obsoleto e inseguro.
*   **HIGH:**
    *   `routes/task_routes.py`: Validações duplicadas para status e prioridade de tarefas.
*   **MEDIUM:**
    *   `app.py`: `SECRET_KEY` hardcoded.
    *   `routes/user_routes.py`: O endpoint `/login` retorna o hash da senha no objeto `user`.
*   **LOW:**
    *   `models/task.py`: O método `is_overdue` não considera timezone, o que pode causar imprecisões.

## Como Rodar:

```bash
pip install -r requirements.txt
python app.py
```

A aplicação roda em `http://localhost:5000`.
