# skills-audit

[![validate](https://github.com/andreischuaste12-ctrl/skills-audit/actions/workflows/validate.yml/badge.svg)](https://github.com/andreischuaste12-ctrl/skills-audit/actions/workflows/validate.yml)

Skill `improve-skills-konvert`: auditoria e melhoria de skills de agentes de IA, baseada em evidências. Analisa ativação, fluxo, referências, segurança e cobertura de avaliação; pesquisa lacunas materiais; e recomenda manter, melhorar, dividir, unificar ou retirar de uso cada skill.

Idioma: português do Brasil (termos técnicos em inglês). Versão: não publicada (ver `CHANGELOG.md`).

## Escopo

Decisões de escopo, definidas pelo mantenedor em 30/10/2026:

- **Público:** projeto open source público, para quem mantém skills pessoais ou de equipe e precisa decidir o que corrigir, unificar ou aposentar. Contribuições seguem `CONTRIBUTING.md`; vulnerabilidades, `SECURITY.md`.
- **Host principal:** Claude Code. Codex é alvo secundário, pela presença de `agents/openai.yaml`. Nenhum dos dois tem compatibilidade comprovada por execução (ver "Estado de verificação"). Compatibilidade de formato (os arquivos seguem a estrutura de skill) não é compatibilidade de comportamento (o agente se comporta como esperado).
- **Entregável padrão:** achados com local, evidência, severidade e confiança; recomendação por skill; mudanças feitas; verificações executadas e não executadas.

### Esta skill ou `skill-creator`?

| Pedido | Destino |
| --- | --- |
| Diagnosticar, revisar ou otimizar uma skill existente | Esta skill |
| Comparar skills, detectar duplicidade, decidir unificar | Esta skill |
| Validar regressão após alterar uma skill | Esta skill |
| Criar uma skill do zero | `skill-creator` |
| Edição pontual sem auditoria (ex.: trocar `default_prompt`) | `skill-creator` |
| Auditar site, SEO ou código sem skill como alvo | Nenhuma das duas |

Se `skill-creator` não estiver disponível, a skill informa isso e oferece instalá-lo ou seguir com o fluxo de auditoria por escolha explícita; não executa a auditoria completa em silêncio.

## Estrutura

| Caminho | Função |
| --- | --- |
| `SKILL.md` | Fluxo em 6 etapas: alvo, inspeção, pesquisa, melhorias, verificação, entrega |
| `references/audit-criteria.md` | Critérios de auditoria, prioridades e esquema único de achado |
| `references/research-and-validation.md` | Quando e até onde pesquisar, níveis de validação, fontes e sua manutenção |
| `references/colecoes-e-unificacao.md` | Protocolo para coleções: inventário, sobreposição, destino e unificação |
| `agents/openai.yaml` | Metadados de interface (Codex/OpenAI) |
| `evals/evals.json` | 21 cenários com asserções, comportamentos proibidos e gravidade |
| `evals/files/` | Fixtures dos cenários (extensão `.txt`, para não serem descobertas como skills) |
| `evals/RESULTS.md` | Critérios de aprovação, falhas críticas e registro de execuções |
| `scripts/validate.py`, `scripts/test_validate.py` | Validação estrutural e seus testes |
| `requirements-dev.txt` | Dependência de desenvolvimento do validador (PyYAML, versão fixada) |
| `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` | Licença MIT, guia de contribuição e política de segurança |
| `CHANGELOG.md` | Histórico de mudanças |
| `RELEASING.md` | Versionamento, critérios de release e o que exige reexecução dos evals |
| `.github/pull_request_template.md` | Checklist de PR |

## Instalação e atualização

O nome da skill (`improve-skills-konvert`) é o que o host usa; o nome deste repositório (`skills-audit`) é só do projeto. Instale copiando o pacote para uma pasta com o nome da skill:

```bash
mkdir -p ~/.claude/skills/improve-skills-konvert
cp -r SKILL.md agents references evals scripts ~/.claude/skills/improve-skills-konvert/
```

O repositório é a fonte do pacote. Em uso, a skill precisa de `SKILL.md`, `references/` e `agents/`; `evals/` e `scripts/` são ativos de manutenção, e o `SKILL.md` aponta para `evals/` (se omitir a pasta, esses links ficam quebrados na cópia instalada). Para atualizar, repita a cópia sobre a pasta instalada, sem criar uma segunda instalação. O diretório de skills de outros hosts pode ser diferente; confirme na documentação do host. O validador emite um aviso (não um erro) quando a pasta do repositório difere do `name`, porque a documentação do Claude Code não exige que coincidam.

## Validação

Requer Python 3 e PyYAML (somente para desenvolvimento, versão fixada em `requirements-dev.txt`). Testado localmente em Python 3.11, 3.12 e 3.13 com PyYAML 6.0.2; o CI roda a mesma matriz. Outras versões não foram testadas.

```bash
pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p "test_*.py"
```

O primeiro comando analisa o frontmatter e `agents/openai.yaml` com parser YAML (chave duplicada é erro) e confere tipos, links, caminhos citados, evals (estrutura, tipos, campos condicionais), fixtures (somente caminhos relativos dentro de `evals/files`), fim de linha e a descrição. Qualquer symlink é erro e o destino não é lido. Cada problema sai com arquivo e motivo; JSON ou YAML com estrutura errada produz erro legível, nunca traceback. Sem PyYAML, o validador termina com código 2 e a instrução de instalação. O segundo comando injeta defeitos de propósito e confere que o validador os detecta.

## Estado de verificação

| Nível | O que é | Estado |
| --- | --- | --- |
| Estrutural | Arquivos, YAML, JSON, links, metadados | Automatizado. O workflow `validate` passou nos commits `bffb94f` e `005bc20` (conferido em 30/10/2026); a versão atual do validador ainda precisa passar no CI após o push |
| Walkthrough | Fluxo aplicado manualmente a um cenário | Não registrado |
| Execução comportamental | Agente roda o cenário no host, com e sem a skill | **Não registrada** (ver `evals/RESULTS.md`) |

Cenário de avaliação não é execução: enquanto não houver linhas em `evals/RESULTS.md`, não há evidência de desempenho nem de compatibilidade de host.

### Hosts validados

Nenhum. Um host só entra nesta tabela depois de instalação, descoberta e invocação testadas, com o smoke test registrado.

| Host | Procedimento de instalação | Descoberta | Invocação | Smoke test | Data |
| --- | --- | --- | --- | --- | --- |
| Claude Code (principal) | não testado | não testada | não testada | não executado | – |
| Codex (secundário) | não testado | não testada | não testada | não executado | – |

Se só um host for testado, ele será declarado como o único host validado.

## Limitações conhecidas

- Sem execução comportamental registrada.
- 6 das 7 fontes de `references/research-and-validation.md` não foram abertas na última conferência (30/10/2026); só a documentação do Claude Code foi lida, parcialmente.
- A proteção de branch exigindo o check `validate` é configuração do GitHub e não foi verificada.
- O CI valida só a estrutura; validar o comportamento exige um agente e custa tokens, então roda manualmente (ver `RELEASING.md`), não a cada PR.
- As ações do workflow usam tags (`@v4`, `@v5`), não SHAs imutáveis.

## Publicar uma alteração

Detalhes e critérios de versão em `RELEASING.md`. Resumo:

1. Rodar os dois comandos de validação.
2. Se mudou `SKILL.md`, referências, fixtures ou critérios, rodar os cenários afetados com e sem a skill e registrar em `evals/RESULTS.md`.
3. Bloquear a publicação se houver erro estrutural ou falha crítica (lista em `evals/RESULTS.md`).
4. Atualizar `CHANGELOG.md` e registrar as limitações da versão.
5. Conferir o resultado do workflow `validate` no commit publicado e, para tornar a verificação obrigatória, exigir os checks do job `structure` (um por versão do Python) na proteção de branch do GitHub.

## Licença

[MIT](LICENSE).
