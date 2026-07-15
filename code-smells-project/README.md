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

## Análise Manual de Problemas

Identificamos os seguintes problemas de arquitetura e qualidade no projeto, classificados por severidade:

- **CRITICAL:**
    - `app.py`: `SECRET_KEY` hardcoded ('minha-chave-super-secreta-123'), expondo a aplicação a riscos de segurança.
    - `models.py`: Vulnerabilidade crítica de SQL Injection em todos os métodos (`get_produto_por_id`, `criar_produto`, `login_usuario`, etc.) devido à concatenação direta de strings.
    - `app.py`: Endpoint `/admin/query` permite a execução de queries SQL arbitrárias pelo cliente, um risco de segurança extremo.
- **HIGH:**
    - `controllers.py`: Padrão "God Class/Fat Controller", onde toda a lógica de negócio, validação e roteamento para quatro domínios está concentrada em um único arquivo.
    - `app.py`: Inicialização da aplicação com `debug=True` ativado, o que expõe stack traces detalhados em caso de erro em produção.
- **MEDIUM:**
    - `models.py`: Problema de performance do tipo "N+1 Queries" nos métodos `get_pedidos_usuario` e `get_todos_pedidos`, executando queries repetitivas em loops.
    - `models.py`: Falta de hash seguro para senhas no método `login_usuario`, armazenando ou comparando senhas em texto puro.
    - `controllers.py`: Tratamento de erros inconsistente, usando `try/except` genérico que retorna `Exception` como string para o cliente, expondo detalhes da estrutura interna.
- **LOW:**
    - `controllers.py`: Uso de `print` para logging em toda a aplicação, em vez de um sistema de logging configurado e estruturado.
    - `app.py`: Validações de input inconsistentes e dispersas pelo código, em vez de um esquema de validação centralizado (ex: Marshmallow).

## Como Rodar:

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.
