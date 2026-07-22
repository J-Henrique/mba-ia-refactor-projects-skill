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

## Análise Manual de Problemas (pós-refatoração)

Problemas identificados durante a auditoria (`reports/audit-project-1.md`), classificados por severidade com justificativa:

- **CRITICAL:**
    - `config/settings.py`: `SECRET_KEY` com fallback hardcoded em dev. *Relevância:* se o código for commitado com a chave de fallback, qualquer um com acesso ao repositório pode forjar sessões. (Corrigido — movido para env var + `.env`)
    - `models/produto_model.py`: SQL Injection histórico por concatenação de strings em queries. *Relevância:* permitia que um usuário malicioso destruísse ou extraísse todo o banco via parâmetros da URL. (Corrigido — placeholders `?` do SQLite)
- **HIGH:**
    - `controllers/`: Lógica de validação ainda nos controllers, poderia ser extraída para services. *Relevância:* dificulta testes unitários e reúso das regras de negócio.
    - `app.py`: `DEBUG = True` ativado. *Relevância:* em produção, expõe stack traces completos ao usuário final, vazando detalhes da infraestrutura. (Corrigido — controlado via env var)
- **MEDIUM:**
    - `models/pedido_model.py`: N+1 queries em listagem de pedidos. *Relevância:* a cada pedido listado, uma query extra é feita para carregar itens — com 100 pedidos, são 101 queries em vez de 2. (Pendente)
    - `models/usuario_model.py`: Senha armazenada em texto puro no seed. *Relevância:* qualquer acesso ao arquivo `database.py` expõe credenciais reais. (Corrigido — bcrypt)
- **LOW:**
    - `controllers/`: `print` residual em alguns lugares. *Relevância:* sem níveis de log, não é possível filtrar mensagens por importância em produção.

## Como Rodar

```bash
pip install -r requirements.txt
cp .env.example .env  # ou configure as variáveis
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot com dados de exemplo.

## Auditoria

Relatório completo em [`reports/audit-project-1.md`](../reports/audit-project-1.md).