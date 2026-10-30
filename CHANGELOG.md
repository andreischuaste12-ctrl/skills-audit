# Changelog

Formato: versões mais recentes primeiro. Nenhuma versão foi publicada ainda.

## Não publicado

### Adicionado
- `scripts/validate.py` e `scripts/test_validate.py`: validação estrutural e testes com defeitos injetados.
- Workflow `.github/workflows/validate.yml`.
- `evals/RESULTS.md`: critérios de aprovação, falhas críticas e registro de execuções.
- Evals 14 a 20 (skill-creator ausente, pacote com caminhos perigosos, symlink, comando de instalação suspeito, injeção de instrução, fato datado, metadados incompatíveis) e 18 fixtures.
- Regra de encaminhamento quando `skill-creator` não está disponível.
- Esquema único de achado, limites de pesquisa e tabela de fontes com status de conferência.

- `requirements-dev.txt` (PyYAML 6.0.2) e instalação no CI.
- Eval 21 (homônimos com caminho indicado: edição só da skill pessoal).
- Testes do validador para YAML truncado, tipo incorreto, chave duplicada, YAML de interface malformado, symlinks, fixtures fora de `evals/files` e estrutura inválida de `evals.json` (43 testes).

- `LICENSE` (MIT), `CONTRIBUTING.md` e `SECURITY.md`.
- Matriz de CI (Python 3.11, 3.12 e 3.13), badge de status, `RELEASING.md` e `.github/pull_request_template.md`.

### Alterado
- `scripts/validate.py`: frontmatter e `agents/openai.yaml` passam por parser YAML (chave duplicada é erro); tipos de `evals.json` validados com erro legível; symlinks rejeitados sem leitura do destino; fixtures restritas a caminhos relativos em `evals/files`; falhas inesperadas viram erro, não traceback.
- Eval 6: o agente deve perguntar qual homônimo é o alvo antes de editar; `allowed_changes` vazio.
- `evals/evals.json`: todos os cenários têm `type`, `objective`, `expectations`, `forbidden`, `allowed_changes` e `severity_if_failed`.
- `README.md` reescrito; `agents/openai.yaml` convertido para LF; `.gitattributes` adicionado.

### Pendente
- Execução real dos 21 cenários com e sem a skill.
- Verificação de 6 das 7 fontes externas.
- Validação do host principal (Claude Code): instalação, descoberta, invocação e smoke test.
- Decisão sobre o nome do repositório contra o `name` da skill.
- Habilitar o relato privado de vulnerabilidades e a proteção de branch no GitHub (configurações do repositório).
