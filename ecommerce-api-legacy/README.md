# ecommerce-api-legacy

API de LMS (Learning Management System) em Node.js com o framework Express. Este projeto gerencia o checkout de cursos, inscrições de usuários e relatórios financeiros.

## Estrutura do Projeto:

*   **`package.json`**: Define as dependências do projeto (como `express` e `sqlite3`) e os scripts para executá-lo (ex: `npm start`).
*   **`src/app.js`**: Ponto de entrada da aplicação. Inicializa o servidor Express, configura o uso de JSON, instancia o `AppManager` para gerenciar a lógica e rotas, e inicia o servidor.
*   **`src/AppManager.js`**: Classe central que gerencia:
    *   Inicialização do banco de dados em memória (`:memory:`) com tabelas e dados de exemplo (usuários, cursos, matrículas, pagamentos, logs de auditoria).
    *   Configuração das rotas da API (`/api/checkout`, `/api/admin/financial-report`, `/api/users/:id`), contendo a lógica de negócio de forma centralizada, o que viola a separação de responsabilidades.
*   **`src/utils.js`**: Utilitários diversos:
    *   `config`: Armazena configurações sensíveis hardcoded (credenciais de banco de dados, chaves de API de pagamento, informações de SMTP).
    *   `logAndCache`: Função simples para logging e cacheamento em memória.
    *   `badCrypto`: Implementação de criptografia fraca para senhas.
    *   `totalRevenue`: Variável global não utilizada de forma eficaz.

## Função da Aplicação:

A API oferece funcionalidades para:

*   **Checkout de Cursos**: Permite a inscrição de usuários em cursos com processamento simulado de pagamento.
*   **Relatórios Financeiros Admin**: Gera um relatório financeiro agregado de cursos.
*   **Deleção de Usuários**: Endpoint para deletar usuários, mas que deixa dados órfãos no banco de dados.

Este projeto exemplifica múltiplos "code smells" e problemas de arquitetura/segurança, incluindo credenciais sensíveis hardcoded, criptografia fraca, lógica de negócio centralizada em uma única classe (`AppManager`), callbacks aninhados, e tratamento inadequado de deleção de dados.

## Como Rodar:

```bash
npm install
npm start
```

A aplicação roda na porta configurada em `utils.js` (geralmente 3000).
