# ARCHITECTURE AUDIT REPORT
Project: ecommerce-api-legacy
Stack: Node.js + Express
Files: 3 analyzed | ~181 lines of code

## Summary
CRITICAL: 2 | HIGH: 4 | MEDIUM: 3 | LOW: 2

## Findings

### [CRITICAL] Hardcoded Credentials
File: `src/utils.js`:2-7
Description: Database credentials (dbUser: "admin_master", dbPass: "senha_super_secreta_prod_123"), payment gateway key ("pk_live_1234567890abcdef"), and SMTP user are hardcoded in plain text in the source code.
Impact: Exposição total de credenciais de produção. Qualquer pessoa com acesso ao repositório pode usar a chave do gateway de pagamento e acessar o banco de dados. Risco de segurança altíssimo.
Recommendation: Mover todas as credenciais para variáveis de ambiente (process.env) com fallback para string vazia. Centralizar em `config/config.js`. Criar arquivo `.env` com os valores e adicionar `.env` ao `.gitignore`.

### [CRITICAL] God Class
File: `src/AppManager.js`:4-139
Description: A classe `AppManager` concentra absolutamente toda a lógica da aplicação: inicialização do banco de dados (initDb), definição de rotas (setupRoutes), lógica de negócio de checkout (pagamento, matrícula, criação de usuário), relatório financeiro, e deleção de usuários.
Impact: Impossível testar unitariamente. Qualquer mudança em uma funcionalidade pode quebrar outra. Código difícil de manter e escalar.
Recommendation: Extrair cada responsabilidade para camadas separadas (MVC): Models para acesso a dados, Controllers para lógica de negócio, Routes para definição de endpoints. Aplicar injeção de dependência para o Database.

### [HIGH] Sensitive Data Logging
File: `src/AppManager.js`:45
Description: `console.log(\`Processando cartão ${cc} na chave ${config.paymentGatewayKey}\`);` — Loga o número completo do cartão de crédito e a chave do gateway de pagamento, ambos em texto puro.
Impact: Violação de PCI-DSS. Números de cartão de crédito em logs de console expõem dados sensíveis dos clientes. A chave do gateway permite processar pagamentos fraudulentos. Risco de multas regulatórias e responsabilidade civil.
Recommendation: Remover completamente o log do cartão e da chave. Se necessário para auditoria, mostrar apenas os 4 últimos dígitos.

### [HIGH] Fat Controller (Fat Route Handler)
File: `src/AppManager.js`:28-78
Description: O endpoint `/api/checkout` (linhas 28-78) contém toda a lógica de negócio inline: validação de dados, busca de curso no banco, busca de usuário por email, criação de usuário com hash de senha, processamento de pagamento e matrícula, criação de matrícula, inserção de pagamento, e log de auditoria — tudo aninhado em callbacks dentro de um único handler de rota.
Impact: Acoplamento extremo. Lógica de negócio não pode ser reutilizada em outros endpoints. Testar o fluxo de checkout requer disparar requisições HTTP completas. Código difícil de ler devido ao callback hell.
Recommendation: Extrair a lógica de checkout para um `CheckoutController` com métodos separados. Mover o acesso a dados para Models. A rota deve apenas chamar o controller.

### [HIGH] Tight Coupling (Sem Injeção de Dependência)
File: `src/AppManager.js`:7
Description: `this.db = new sqlite3.Database(':memory:');` — A classe `AppManager` instancia diretamente o banco de dados em seu construtor. Não há como injetar uma dependência mockada para testes.
Impact: Impossível testar unitariamente o `AppManager`. Os testes obrigatoriamente usariam o banco real em memória, tornando-os lentos e com estado compartilhado.
Recommendation: Receber a instância do banco via construtor (injeção de dependência): `constructor(db) { this.db = db; }`. A composição deve ser feita no entry point (`app.js`).

### [HIGH] Deprecated / Insecure Cryptography
File: `src/utils.js`:17-23
Description: A função `badCrypto` implementa um hash de senha caseiro baseado em Base64 repetido 10.000 vezes e truncado para 10 caracteres. Não utiliza bcrypt, que já está disponível como dependência do projeto (`bcryptjs`).
Impact: Senhas armazenadas com hash extremamente fraco. Um atacante que obtenha acesso ao banco pode facilmente reverter os hashes e obter as senhas dos usuários em texto puro.
Recommendation: Substituir `badCrypto` pelo uso de `bcryptjs` (já disponível em package.json) com `bcrypt.hashSync(password, saltRounds)` ou a versão async.

### [MEDIUM] N+1 Queries (Gargalo de Performance)
File: `src/AppManager.js`:83-128
Description: No endpoint `/api/admin/financial-report`, para cada curso encontrado (linha 89), é feita uma query para buscar matrículas. Para cada matrícula (linha 102), são feitas mais duas queries (usuário e pagamento). Total de ~1 + N*M queries onde N=cursos e M=matrículas.
Impact: Degradação severa de performance conforme o número de cursos e matrículas cresce. Para 100 cursos com 50 matrículas cada, seriam ~5.001 queries.
Recommendation: Substituir por queries com JOIN (SQL) para buscar todos os dados em uma única consulta, ou no máximo 3 queries separadas (cursos, matrículas com usuários, pagamentos).

### [MEDIUM] Duplicate Code (Tratamento de Erro Repetido)
File: `src/AppManager.js`:37-57
Description: Padrão `if (err) return res.status(500).send("Erro...")` repetido em múltiplos callbacks. As mensagens de erro são strings soltas sem padronização.
Impact: Manutenção dificultada — qualquer mudança no formato de erro exige alterar dezenas de locais. Inconsistência nas respostas de erro da API.
Recommendation: Implementar um middleware de erro centralizado (Express error handler) que capture todas as exceções. Usar `next(err)` nos callbacks em vez de `res.status(500).send(...)`.

### [MEDIUM] Configurações Dispersas
File: `src/utils.js`:1-7, `src/app.js`:12
Description: Configurações estão divididas entre `src/utils.js` (porta, credenciais) e `src/app.js` (uso da porta). Não há um arquivo de configuração centralizado. O `.env.example` existe mas não é lido pelo código — o `dotenv` está instalado mas não é utilizado.
Impact: Dificuldade de configurar a aplicação para diferentes ambientes (dev, staging, prod). Configurações misturadas com código utilitário.
Recommendation: Criar `config/config.js` que carregue `dotenv` e centralize todas as configurações com fallback seguro. Remover configurações de `utils.js`.

### [LOW] Inconsistent Naming (Variáveis Crípticas)
File: `src/AppManager.js`:29-33
Description: Nomes de variáveis extremamente curtos e sem significado: `u` (user), `e` (email), `p` (password), `cid` (course id), `cc` (credit card), `enrId` (enrollment id).
Impact: Dificulta a compreensão do código por outros desenvolvedores. Aumenta o custo de manutenção e o risco de bugs causados por interpretação incorreta.
Recommendation: Renomear para nomes descritivos: `userName`, `email`, `password`, `courseId`, `cardNumber`, `enrollmentId`.

### [LOW] Magic Numbers
File: `src/utils.js`:19-22
Description: Valores numéricos mágicos sem explicação: `10000` (número de iterações do loop) e `10` (limite da substring). Não há constantes nomeadas explicando o significado.
Impact: Dificulta a compreensão do propósito dos números. Qualquer alteração requer caçar o número no código.
Recommendation: Extrair para constantes nomeadas: `const HASH_ITERATIONS = 10000;` e `const HASH_LENGTH = 10;`

---
Total: 11 findings
---
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]