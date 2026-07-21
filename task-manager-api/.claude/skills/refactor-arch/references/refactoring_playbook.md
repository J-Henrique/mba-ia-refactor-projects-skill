# Playbook de Refatoração

Este playbook contém padrões concretos de transformação para corrigir os anti-patterns identificados e mover o projeto para o padrão MVC.

## Padrões de Refatoração

### 1. Extração de Hardcoded Credentials
- **Antes:** `SECRET_KEY = 'minha-chave-secreta'`
- **Depois:** Carregar de variável de ambiente `os.environ.get('SECRET_KEY')` ou arquivo `.env`.

### 2. Extração de Lógica de Controller (Fat Controller -> MVC)
- **Antes:** Lógica SQL e de negócio dentro de `route` do Flask.
- **Depois:** Rota chama o Controller, que chama o Model/Service.

### 3. Extração de Model (God Class -> Models)
- **Antes:** Consultas SQL espalhadas no `app.py`.
- **Depois:** Criar classe específica no diretório `models/` estendendo `db.Model`.

### 4. Implementação de Middleware de Erro
- **Antes:** `try/except` repetido em todas as rotas.
- **Depois:** Decorador `@app.errorhandler` para capturar exceções globalmente.

### 5. Substituição de API Deprecated
- **Antes:** `hashlib.md5(senha)`
- **Depois:** Utilizar bibliotecas robustas de hash (ex: `bcrypt` ou `werkzeug.security`).

### 6. Injeção de Dependência
- **Antes:** Importação direta de objetos de banco/config dentro de funções.
- **Depois:** Passar dependências como argumentos para funções ou construtores de classes.

### 7. Centralização de Configurações
- **Antes:** Configurações soltas no `app.py`.
- **Depois:** Classe `Config` em `config/settings.py`.

### 8. Remoção de Duplicate Code
- **Antes:** Código idêntico em múltiplas rotas.
- **Depois:** Extrair lógica comum para métodos utilitários ou Services.
