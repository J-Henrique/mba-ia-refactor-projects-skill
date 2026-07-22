================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   6 source files analyzed | ~250 lines of code

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Callback Hell / Asynchronous Complexity
File: src/controllers/CheckoutController.js:13-73
Description: Rota de checkout possui múltiplos níveis de `new Promise()` aninhados para consultas sequenciais ao DB (curso, usuário, enrollment, payment, audit_log).
Impact: Altíssimo risco de race conditions, difícil manutenção e legibilidade.
Recommendation: Refatorar para utilizar async/await com `util.promisify` ou um wrapper de banco que retorne promises.

### [CRITICAL] Insecure Password Storage
File: src/models/Database.js:11
Description: Senha do usuário "Leonan" armazenada como texto puro (`'123'`) no seed do banco em memória.
Impact: Credenciais expostas — qualquer um com acesso ao processo consegue ler.
Recommendation: Utilizar `hashPassword()` de `utils/security.js` no seed, ou aplicar hash antes de inserir.

### [HIGH] Missing Routes Separation
File: src/app.js:11-13
Description: Rotas definidas inline no `app.js` em vez de arquivo dedicado em `routes/`.
Impact: Viola separação de responsabilidades — dificulta localizar e modificar endpoints.
Recommendation: Extrair rotas para `src/routes/index.js` e usar `app.use(router)`.

### [HIGH] Data Inconsistency — Transaction Scope
File: src/controllers/UserController.js:9-26
Description: `db.serialize()` usado para transação manual, mas `serialize` não é uma transação real — filas de execução concorrentes podem intercalar operações.
Impact: Possível corrupção de dados em cenários de alta concorrência.
Recommendation: Usar `db.run("BEGIN")` / `db.run("COMMIT")` com callback chain, ou migrar para `better-sqlite3` que oferece transações síncronas.

### [MEDIUM] Improper Error Handling
File: src/controllers/CheckoutController.js:78
Description: Retorno de erro como texto puro (`res.status(500).send("Erro interno")`) em vez de JSON.
Impact: Dificulta debugging e não segue padrão REST.
Recommendation: Usar `res.status(500).json({ error: "..." })` e middleware de erro centralizado.

### [MEDIUM] Console Logging
File: src/controllers/CheckoutController.js:77, src/controllers/UserController.js:31, src/controllers/ReportController.js:52
Description: Uso de `console.error` para tracking de fluxo em vez de logger estruturado.
Impact: Falta de níveis de log, timestamps e formato estruturado.
Recommendation: Implementar biblioteca `winston` ou `pino` para logging.

### [LOW] Hardcoded In-Memory Database
File: src/models/Database.js:2
Description: Banco SQLite em memória (`:memory:`) — todos os dados são perdidos ao reiniciar o servidor.
Impact: Dados de seed recriados a cada restart, impossível uso em produção.
Recommendation: Usar arquivo `.db` em disco para desenvolvimento, variável de ambiente para produção.

---
Total: 7 findings
---

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]