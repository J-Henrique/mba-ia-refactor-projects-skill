# Catálogo de Anti-patterns

Este catálogo lista os anti-patterns que a skill `refactor-arch` deve identificar, classificados por severidade.

| Anti-pattern | Severidade | Descrição | Impacto |
| :--- | :--- | :--- | :--- |
| God Class | CRITICAL | Classe ou arquivo contendo toda a lógica (negócio, banco, rotas). | Impossível testar ou manter. |
| Hardcoded Credentials | CRITICAL | Senhas, chaves de API expostas no código. | Risco de segurança altíssimo. |
| SQL Injection Vulnerability | CRITICAL | Concatenação direta de strings em queries SQL. | Exposição/destruição de dados. |
| Fat Controller | HIGH | Controller contendo lógica de negócio complexa além de roteamento. | Acoplamento, difícil reutilização. |
| Tight Coupling | HIGH | Componentes fortemente acoplados sem injeção de dependência. | Difícil substituição/teste. |
| N+1 Queries | MEDIUM | Queries executadas dentro de loops. | Gargalo grave de performance. |
| Duplicate Code | MEDIUM | Lógica idêntica repetida em múltiplos locais. | Dificulta manutenibilidade. |
| Magic Numbers | LOW | Valores numéricos sem significado claro no código. | Dificulta a compreensão. |
| Inconsistent Naming | LOW | Nomenclatura que não segue padrões da linguagem. | Baixa legibilidade. |
| Deprecated API Usage | MEDIUM | Uso de bibliotecas ou métodos obsoletos (ex: `hashlib.md5`). | Risco de segurança/incompatibilidade. |
