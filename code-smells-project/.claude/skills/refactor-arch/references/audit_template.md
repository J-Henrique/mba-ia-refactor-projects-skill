# Template de Relatório de Auditoria

Este é o formato padronizado que a skill deve seguir ao gerar o relatório na Fase 2.

---
# ARCHITECTURE AUDIT REPORT
Project: {{projeto_nome}}
Stack: {{linguagem}} + {{framework}}
Files: {{total_arquivos}} analyzed | ~{{total_linhas}} lines of code

## Summary
CRITICAL: {{cont_critical}} \| HIGH: {{cont_high}} \| MEDIUM: {{cont_medium}} \| LOW: {{cont_low}}

## Findings

### [{{severidade}}] {{nome_do_anti_pattern}}
File: {{arquivo}}:{{linha}}
Description: {{descricao_detalhada}}
Impact: {{impacto_no_negocio_ou_manutencao}}
Recommendation: {{passo_a_passo_da_correcao}}

... (repetir para cada achado)

---
Total: {{total_findings}} findings
---
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
