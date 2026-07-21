# Heurísticas de Análise de Projeto

Para detectar a stack e o contexto do projeto, utilize as seguintes heurísticas:

## 1. Detecção de Linguagem e Framework
- **Python:** Procurar por `requirements.txt`, `Pipfile` ou `pyproject.toml`.
  - **Flask:** Procurar por `flask` no `requirements.txt`.
  - **Django:** Procurar por `django` no `requirements.txt`.
- **Node.js:** Procurar por `package.json`.
  - **Express:** Procurar por `express` nas dependências do `package.json`.

## 2. Mapeamento de Arquitetura
- **Estrutura de diretórios:**
  - Identificar pastas como `models/`, `routes/`, `controllers/`, `services/`, `utils/`.
  - Se todos os arquivos estiverem na raiz ou em poucos arquivos (ex: `app.py`), classificar como **Monolítico/Desestruturado**.
  - Se houver pastas separando responsabilidades, classificar como **Estruturado/Camadas**.

## 3. Identificação de Banco de Dados
- **SQLAlchemy/Flask-SQLAlchemy:** Presença de arquivos de modelo usando `db.Model`.
- **ORM-less/Raw SQL:** Presença de consultas SQL brutas (`SELECT`, `INSERT`) dentro de rotas ou arquivos de lógica.
- **SQLite:** Presença de arquivos `.db` ou `sqlite` nas configurações.

## 4. Domínio da Aplicação
- Analisar os nomes dos arquivos e rotas (ex: `task_routes.py` -> Gerenciamento de Tarefas).
- Ler os comentários iniciais e `README.md` (se disponível) para confirmar o propósito do sistema.
