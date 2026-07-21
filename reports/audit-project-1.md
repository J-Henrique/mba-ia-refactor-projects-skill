# ARCHITECTURE AUDIT REPORT
Project: code-smells-project
Stack: Python + Flask
Files: 4 analyzed | ~800 lines of code

## Summary
CRITICAL: 3 | HIGH: 2 | MEDIUM: 3 | LOW: 1

## Findings

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
Impact: Risco alto de segurança em produção.
Recommendation: Mover para variáveis de ambiente ou arquivo .env seguro.

### [CRITICAL] SQL Injection Vulnerability
File: models.py:34, 46, 56, 127, 245
Description: Concatenação direta de strings em queries SQL.
Impact: Risco altíssimo de manipulação/exclusão de dados.
Recommendation: Utilizar placeholders (?) do SQLite para parâmetros.

### [CRITICAL] Insecure Admin Query Endpoint
File: app.py:53
Description: Endpoint `/admin/query` permite execução de queries arbitrárias.
Impact: Risco de segurança extremo.
Recommendation: Remover endpoint ou restringir acesso estritamente a administradores via autenticação robusta.

### [HIGH] God Class / Fat Controller
File: controllers.py:1-250
Description: Arquivo centraliza toda lógica de negócio e roteamento para 4 domínios.
Impact: Alta dificuldade de manutenção e teste.
Recommendation: Refatorar para separar responsabilidades por domínio (MVC).

### [HIGH] Debug Mode On
File: app.py:9
Description: `DEBUG = True` ativado em app.config.
Impact: Exposição de stack traces detalhados em caso de erro.
Recommendation: Desativar debug em ambiente de produção.

### [MEDIUM] N+1 Queries
File: models.py:228
Description: Consultas SQL dentro de loop em get_pedidos_usuario.
Impact: Performance lenta em listas grandes.
Recommendation: Usar JOIN SQL para carregar dados em uma única query.

### [MEDIUM] Insecure Password Storage
File: models.py:118
Description: Armazenamento ou comparação de senha sem hash seguro.
Impact: Risco de vazamento de credenciais.
Recommendation: Utilizar biblioteca `bcrypt` para hashing de senhas.

### [MEDIUM] Inconsistent Error Handling
File: controllers.py:9, 105
Description: Uso de `try/except` retornando str(e) para o cliente.
Impact: Vazamento de informações internas da estrutura da aplicação.
Recommendation: Centralizar tratamento de erros e retornar mensagens amigáveis.

### [LOW] Verbose Logging
File: controllers.py:7
Description: Uso excessivo de `print` para logs.
Impact: Dificulta rastreabilidade e análise em produção.
Recommendation: Implementar biblioteca `logging` padrão do Python.

---
Total: 9 findings
---
