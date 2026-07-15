# Skill: Refactor Arch

Esta skill automatiza a análise, auditoria e refatoração de projetos legados para o padrão MVC.

## Uso
Execute com: `refactor-arch`

---

## Fase 1 — Análise (Project Analysis)
Utilize `references/analysis_heuristics.md` para:
1. Detectar a linguagem (Python/Node) e o framework (Flask/Express).
2. Mapear a arquitetura atual e o domínio do projeto.
3. Imprimir um relatório com:
   - Stack detectada
   - Domínio da aplicação
   - Estrutura de diretórios
   - Resumo da codebase

---

## Fase 2 — Auditoria (Architecture Audit)
Utilize `references/anti_patterns.md` e `references/audit_template.md` para:
1. Analisar a codebase em busca de anti-patterns (CRITICAL a LOW).
2. Gerar um relatório estruturado seguindo `references/audit_template.md`.
3. **OBRIGATÓRIO:** Pausar e solicitar confirmação do usuário antes de proceder para a fase de refatoração.
   - Pergunta: "Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]"

---

## Fase 3 — Refatoração (Refactoring)
Utilize `references/mvc_guidelines.md` e `references/refactoring_playbook.md` para:
1. Reestruturar o projeto conforme o padrão MVC:
   - Criar estrutura `models/`, `controllers/`, `views/` (ou `routes/`).
   - Mover lógica de negócio para controllers/services.
   - Mover lógica de dados para models.
   - Extrair configurações para `config/`.
2. Aplicar as transformações definidas no `references/refactoring_playbook.md`.
3. Validar o resultado:
   - Verificar se a aplicação inicializa sem erros.
   - Validar se os endpoints originais continuam funcionando.
   - Imprimir o resumo das mudanças realizadas e a nova estrutura de diretórios.
