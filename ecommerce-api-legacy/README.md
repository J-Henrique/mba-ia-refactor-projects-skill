# ecommerce-api-legacy

LMS API (Node.js/Express) com fluxo de checkout.

## Análise Manual de Problemas

Identificamos os seguintes problemas de arquitetura e qualidade no projeto, classificados por severidade:

- **CRITICAL:**
    - `AppManager.js`: SQL Injection em todas as queries (concatenação direta de strings).
    - `AppManager.js`: Credenciais de gateway de pagamento hardcoded (`config.paymentGatewayKey`).
    - `AppManager.js`: "God Class" (`AppManager`) centraliza DB, rotas, lógica de negócio e geração de relatórios.
- **HIGH:**
    - `AppManager.js`: Criptografia insegura (`badCrypto` function).
    - `AppManager.js`: Falta de validação robusta de entradas.
- **MEDIUM:**
    - `AppManager.js`: Gerenciamento inconsistente de erros e vazamento de status do banco.
    - `utils.js`: Lógica de utilitários acoplada e pouco testável.
- **LOW:**
    - `AppManager.js`: Uso de `console.log` para logs de transações sensíveis.
    - `AppManager.js`: Comentários pobres e código sem indentação consistente.
