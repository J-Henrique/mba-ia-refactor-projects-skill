================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask-SQLAlchemy
Files:   Multiple analyzed

## Summary
CRITICAL: 1 | HIGH: 3 | MEDIUM: 3 | LOW: 1

## Findings

### [CRITICAL] Exception Swallowing / Generic Error Handling
File: task_routes.py:32
Description: O bloco `try...except` na rota `get_tasks` silencia todos os erros (`except: return...`), dificultando o diagnóstico de problemas reais.
Impact: Falha em debugar erros críticos do banco de dados ou da aplicação.
Recommendation: Capturar exceções específicas e registrar logs adequados.

### [HIGH] Fat Routes / Logic in Blueprints
File: task_routes.py
Description: As rotas contêm lógica excessiva de negócio, formatação de dados e validações, violando o padrão MVC.
Impact: Baixa manutenibilidade e alta dificuldade de teste unitário.
Recommendation: Mover a lógica de negócio para uma camada de Service/Controller.

### [HIGH] Missing Transactional Integrity
File: task_routes.py:116
Description: Operações de banco de dados sem uso explícito de transações em fluxos complexos.
Impact: Risco de corrupção de dados em caso de falha parcial.
Recommendation: Utilizar `db.session.begin()` ou gerentes de transação.

### [HIGH] Hardcoded Secret Key
File: app.py:13
Description: `SECRET_KEY` definida diretamente no código.
Impact: Exposição de segredo em caso de acesso ao repositório.
Recommendation: Utilizar variáveis de ambiente (.env).

### [MEDIUM] Code Duplication
File: task_routes.py
Description: Lógica de validação de `overdue` repetida em `get_tasks` e `get_task`.
Impact: Dificuldade de manter a consistência da regra de negócio.
Recommendation: Centralizar a regra de negócio no Model (`Task`).

### [MEDIUM] Improper Date Handling
File: task_routes.py:102, 169
Description: Uso de `datetime.utcnow()` que é deprecated em versões recentes do Python.
Impact: Possível erro futuro de compatibilidade.
Recommendation: Atualizar para o uso de timezone-aware datetimes.

### [LOW] Verbose Print Statements
File: task_routes.py:124, 185
Description: Uso de `print()` em vez de logging estruturado.
Impact: Logs não seguem padrões de produção.
Recommendation: Implementar biblioteca `logging`.

---
Total: 8 findings
---
