# Diretrizes de Arquitetura MVC

Esta guia define a estrutura e responsabilidades das camadas no padrão MVC que a skill deve aplicar durante a refatoração.

## Estrutura Alvo (MVC)

- **Models:** Responsáveis exclusivamente pela persistência e modelagem dos dados. Não devem conter lógica de roteamento ou formatação de resposta.
- **Controllers:** Orquestram o fluxo da aplicação. Recebem a requisição, chamam o Model (ou Services, se necessário), processam o resultado e enviam a resposta (ou renderizam a View).
- **Views (ou Routes/API Layer):** Responsáveis por definir os endpoints, validar o input básico do usuário e chamar o Controller apropriado.
- **Config:** Armazenamento centralizado de configurações (chaves, URLs, conexões de banco) para evitar hardcoding.
- **Error Handling:** Middleware ou handler centralizado para capturar exceções e retornar respostas padronizadas.

## Princípios de Responsabilidade

1.  **Separação:** Nenhuma camada deve conhecer detalhes de implementação de outra camada além da interface pública.
2.  **Configuração:** Zero segredos ou configurações específicas de ambiente hardcoded no código fonte.
3.  **Injeção:** Utilizar injeção de dependência para evitar acoplamento forte entre componentes.
