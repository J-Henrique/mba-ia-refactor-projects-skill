================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express
Files:   3 analyzed | ~250 lines of code

## Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [CRITICAL] Callback Hell / Asynchronous Complexity
File: AppManager.js:setupRoutes
Description: Rota de checkout possui múltiplos níveis de nesting (callbacks aninhados) para consultas sequenciais ao DB.
Impact: Altíssimo risco de race conditions, difícil manutenção e legibilidade.
Recommendation: Refatorar para utilizar async/await.

### [CRITICAL] Insecure Cryptography / Weak Authentication
File: utils.js:badCrypto
Description: Uso de criptografia própria não segura (badCrypto) para hashes de senha.
Impact: Facilmente reversível, comprometendo credenciais.
Recommendation: Utilizar bcrypt ou argon2.

### [HIGH] God Object
File: AppManager.js
Description: AppManager centraliza DB initialization, roteamento e lógica de negócio.
Impact: Violação do Single Responsibility Principle.
Recommendation: Separar em Controllers, Models e Services.

### [HIGH] Data Inconsistency
File: AppManager.js:DELETE /api/users/:id
Description: Deleta usuário sem tratar registros relacionados (enrollments/payments).
Impact: Database corruption (dirty data).
Recommendation: Implementar transações ou deleção em cascata.

### [MEDIUM] Improper Error Handling
File: AppManager.js
Description: Retorno inconsistente de erros (`res.status(500).send("Erro...")`).
Impact: Difícil debugging e falta de feedback claro para cliente.
Recommendation: Middleware de erro centralizado.

### [LOW] Console Logging
File: AppManager.js
Description: Uso de `console.log` para tracking de fluxo.
Impact: Falta de estruturação de logs.
Recommendation: Implementar biblioteca `winston` ou `pino`.

---
Total: 7 findings
---
