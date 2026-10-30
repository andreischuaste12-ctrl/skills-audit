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

### Alterado
- `evals/evals.json`: todos os cenários têm `type`, `objective`, `expectations`, `forbidden`, `allowed_changes` e `severity_if_failed`.
- `README.md` reescrito; `agents/openai.yaml` convertido para LF; `.gitattributes` adicionado.

### Pendente
- Execução real dos 20 cenários com e sem a skill.
- Verificação de 6 das 7 fontes externas.
- Definição de licença, do host principal e do formato de distribuição.
