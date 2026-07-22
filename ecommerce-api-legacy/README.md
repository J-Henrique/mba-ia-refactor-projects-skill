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

Problemas identificados durante a auditoria (`reports/audit-project-2.md`), classificados por severidade com justificativa:

- **CRITICAL:**
    - `controllers/CheckoutController.js`: Múltiplos `new Promise()` aninhados (callback hell). *Relevância:* 7 níveis de aninhamento tornam o fluxo de checkout impossível de ler e propenso a race conditions. (Pendente)
    - `models/Database.js`: Senha em texto puro no seed (`'123'`). *Relevância:* qualquer pessoa com acesso ao código consegue extrair credenciais reais do banco em memória. (Pendente)
- **HIGH:**
    - `controllers/UserController.js`: Transação manual com `db.serialize()` não é thread-safe. *Relevância:* em cenários de alta concorrência, operações podem intercalar e corromper o banco.
    - `src/app.js`: Antes as rotas eram inline no `app.js`. *Relevância:* violava separação de responsabilidades — para adicionar um endpoint, era necessário modificar o entry point da aplicação. (Corrigido — extraído para `routes/index.js`)
- **MEDIUM:**
    - `controllers/`: Retorno de erro como texto puro em alguns lugares. *Relevância:* clientes que esperam JSON quebram ao receber `res.send("Erro")` — sem `Content-Type: application/json`. (Corrigido — agora JSON)
    - `controllers/`: `console.error` para logging. *Relevância:* sem timestamps, níveis ou formato estruturado, é impossível fazer debugging em produção.
- **LOW:**
    - `models/Database.js`: Banco em `:memory:`. *Relevância:* todos os dados são perdidos ao reiniciar o servidor, inviável para qualquer ambiente que não seja desenvolvimento.

## Como Rodar

```bash
npm install
cp .env.example .env  # configure as variáveis
npm start
```

A aplicação sobe em `http://localhost:3000`.

## Auditoria

Relatório completo em [`reports/audit-project-2.md`](../reports/audit-project-2.md).