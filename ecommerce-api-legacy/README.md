# ecommerce-api-legacy

API de LMS (Learning Management System) em Node.js/Express com fluxo de checkout e matrícula. Projeto refatorado para o padrão **MVC**.

## Stack

- **Linguagem:** Node.js
- **Framework:** Express
- **Banco:** SQLite (via `sqlite3` — em memória para dev)
- **Autenticação:** `bcryptjs`

## Estrutura (MVC)

```
ecommerce-api-legacy/
├── src/
│   ├── app.js                    # Entry point — inicializa app, middleware de erro
│   ├── config/
│   │   └── config.js             # Configuração centralizada via env vars
│   ├── controllers/              # Lógica de negócio + tratamento HTTP
│   │   ├── CheckoutController.js
│   │   ├── ReportController.js
│   │   └── UserController.js
│   ├── models/
│   │   └── Database.js           # Inicialização SQLite + seed
│   ├── routes/
│   │   └── index.js              # Definição de endpoints (Router)
│   └── utils/
│       └── security.js           # Hash de senha (bcryptjs)
├── package.json
└── .env.example
```

## Funcionalidades

- **Checkout:** Matrícula em curso com validação de pagamento (cartão começando com `4` = aprovado)
- **Relatórios:** Relatório financeiro com JOIN entre cursos, matrículas, usuários e pagamentos
- **Usuários:** Deleção de usuário com remoção em cascata de registros relacionados

## Análise Manual de Problemas (pós-refatoração)

Problemas identificados durante a auditoria (`reports/audit-project-2.md`):

- **CRITICAL:**
    - `controllers/CheckoutController.js`: Múltiplos `new Promise()` aninhados (callback hell) — pendente
    - `models/Database.js`: Senha em texto puro no seed (`'123'`) — pendente
- **HIGH:**
    - `controllers/UserController.js`: Transação manual com `db.serialize()` não é thread-safe
    - `src/app.js`: Antes as rotas eram inline (corrigido — extraído para `routes/index.js`)
- **MEDIUM:**
    - `controllers/`: Retorno de erro como texto puro em alguns lugares (corrigido — agora JSON)
    - `controllers/`: `console.error` para logging (sem logger estruturado)
- **LOW:**
    - `models/Database.js`: Banco em `:memory:` — dados voláteis

## Como Rodar

```bash
npm install
cp .env.example .env  # configure as variáveis
npm start
```

A aplicação sobe em `http://localhost:3000`.

## Auditoria

Relatório completo em [`reports/audit-project-2.md`](../reports/audit-project-2.md).