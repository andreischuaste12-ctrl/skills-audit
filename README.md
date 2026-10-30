# skills-audit

Skill `improve-skills-konvert`: auditoria e melhoria de skills de agentes de IA, baseada em evidências. Analisa ativação, fluxo, referências, segurança e cobertura de avaliação; pesquisa lacunas materiais; e recomenda manter, melhorar, dividir, unificar ou retirar de uso cada skill.

Idioma: português do Brasil (termos técnicos em inglês). Versão: não publicada (ver `CHANGELOG.md`).

## Escopo

Premissas de escopo, a confirmar pelo mantenedor:

- **Público:** quem mantém skills pessoais ou de equipe e precisa decidir o que corrigir, unificar ou aposentar.
- **Hosts-alvo:** Claude Code e Codex, pela presença de `SKILL.md` e `agents/openai.yaml`. Nenhum tem compatibilidade comprovada por execução (ver "Estado de verificação").
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
| `evals/evals.json` | 20 cenários com asserções, comportamentos proibidos e gravidade |
| `evals/files/` | Fixtures dos cenários (extensão `.txt`, para não serem descobertas como skills) |
| `evals/RESULTS.md` | Critérios de aprovação, falhas críticas e registro de execuções |
| `scripts/validate.py`, `scripts/test_validate.py` | Validação estrutural e seus testes |
| `CHANGELOG.md` | Histórico de mudanças |

## Instalação e atualização

O nome da skill (`improve-skills-konvert`) é o que o host usa; o nome deste repositório (`skills-audit`) é só do projeto. Instale copiando o pacote para uma pasta com o nome da skill:

```bash
mkdir -p ~/.claude/skills/improve-skills-konvert
cp -r SKILL.md agents references evals scripts ~/.claude/skills/improve-skills-konvert/
```

Para atualizar, repita a cópia sobre a pasta instalada, sem criar uma segunda instalação. O diretório de skills de outros hosts pode ser diferente; confirme na documentação do host. O validador emite um aviso (não um erro) quando a pasta do repositório difere do `name`, porque a documentação do Claude Code não exige que coincidam.

## Validação

Só biblioteca padrão do Python, sem dependências externas. Testado em Python 3.13; o CI usa 3.12. Outras versões não foram testadas.

```bash
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p "test_*.py"
```

O primeiro comando cobre frontmatter, tamanho da descrição, links e caminhos citados, evals (campos, fixtures, coerência de `skill_name`), `agents/openai.yaml` e fim de linha, e informa arquivo e problema. O segundo injeta defeitos de propósito e confere que o validador os detecta.

## Estado de verificação

| Nível | O que é | Estado |
| --- | --- | --- |
| Estrutural | Arquivos, JSON, links, metadados | Automatizado (script e workflow de CI) |
| Walkthrough | Fluxo aplicado manualmente a um cenário | Não registrado |
| Execução comportamental | Agente roda o cenário no host, com e sem a skill | **Não registrada** (ver `evals/RESULTS.md`) |

Cenário de avaliação não é execução: enquanto não houver linhas em `evals/RESULTS.md`, não há evidência de desempenho nem de compatibilidade de host.

## Limitações conhecidas

- Sem execução comportamental registrada.
- 6 das 7 fontes de `references/research-and-validation.md` não foram abertas na última conferência (30/10/2026); só a documentação do Claude Code foi lida, parcialmente.
- Sem licença definida: os direitos de reuso permanecem reservados ao autor até que uma seja escolhida.
- O workflow de CI só tem valor após o primeiro push ao GitHub.

## Publicar uma alteração

1. Rodar os dois comandos de validação.
2. Se mudou `SKILL.md`, referências, fixtures ou critérios, rodar os cenários afetados com e sem a skill e registrar em `evals/RESULTS.md`.
3. Bloquear a publicação se houver erro estrutural ou falha crítica (lista em `evals/RESULTS.md`).
4. Atualizar `CHANGELOG.md` e registrar as limitações da versão.
5. Para tornar a verificação obrigatória, ative a proteção de branch no GitHub exigindo o workflow `validate`.
