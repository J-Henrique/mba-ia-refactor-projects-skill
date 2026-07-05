# code-smells-project

API de E-commerce desenvolvida em Python com o framework Flask, servindo como projeto base para o desafio de refatoração arquitetural (`refactor-arch`).

## Estrutura do Projeto:

*   **`app.py`**: Arquivo principal da aplicação Flask. Responsável por inicializar o servidor, configurar extensões (como `flask-cors`), registrar as rotas que mapeiam para as funções em `controllers.py`, e definir endpoints administrativos.
*   **`controllers.py`**: Contém a lógica de negócio e o tratamento das requisições. Lida com validações de dados de entrada e orquestra as operações chamando as funções do módulo `models.py`.
*   **`models.py`**: Responsável pela interação direta com o banco de dados SQLite (`loja.db`). Define as operações de CRUD (Create, Read, Update, Delete) para os dados de produtos, usuários, pedidos e para a geração de relatórios.
*   **`database.py`**: Gerencia a conexão com o banco de dados SQLite. Cria as tabelas (`produtos`, `usuarios`, `pedidos`, `itens_pedido`) se elas não existirem e popula o banco com dados iniciais ao ser executado pela primeira vez.
*   **`requirements.txt`**: Lista as dependências Python do projeto, como `flask` e `flask-cors`.
*   **`README.md`**: Documentação básica do projeto.

## Função da Aplicação:

A API gerencia um sistema de e-commerce com as seguintes funcionalidades:

*   **Produtos**: Listar, buscar, criar, atualizar e deletar produtos.
*   **Usuários**: Listar, buscar, criar usuários e autenticar via login.
*   **Pedidos**: Criar pedidos (com validação de estoque e produtos), listar todos os pedidos, listar pedidos por usuário e atualizar o status de um pedido.
*   **Relatórios**: Gerar um relatório de vendas.
*   **Administrativo**: Inclui endpoints para resetar o banco de dados e executar queries SQL arbitrárias (representando um risco de segurança).

Este projeto é intencionalmente projetado com várias práticas de código que podem ser consideradas "code smells" ou problemas de arquitetura, como validações repetitivas, manipulação direta de SQL, lógica de negócio misturada com controle de rotas, e credenciais hardcoded, visando ser um bom candidato para o desafio de refatoração.

*   **Problemas Identificados (Análise Manual):**
    *   **CRITICAL:** `SECRET_KEY` hardcoded em `app.py`, manipulação de SQL direta e falta de ORM robusto em `models.py`, lógica de negócio em `controllers.py` misturada com roteamento, `debug=True` em `app.py` implícito, credenciais de banco de dados hardcoded em `database.py`.
    *   **HIGH:** Repetição de validações em `controllers.py`, falta de separação de camadas em `models.py`, ausência de pool de conexões em `database.py`.
    *   **MEDIUM:** Uso de `print` para logs em `controllers.py`, `get_db()` retornando conexão global sem gerenciamento explícito.
    *   **LOW:** Mensagem de root estática em `app.py`.

## Como Rodar:

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.
