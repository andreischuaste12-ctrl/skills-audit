# Releases

Nenhuma versão foi publicada. Este documento define como e quando publicar.

## Versionamento

[SemVer](https://semver.org/lang/pt-BR/) com tags `vX.Y.Z`. Enquanto não houver uma linha de base registrada em `evals/RESULTS.md`, a versão fica em `0.y.z`.

| Mudança | Incremento |
| --- | --- |
| Link, typo ou fixture sem efeito no comportamento | PATCH |
| Instruções, referências, evals ou critérios que alteram o comportamento | MINOR |
| Escopo, nome da skill ou contrato (formato de saída, regras de autorização) | MAJOR |

## O que exige reexecução dos evals

| Arquivo alterado | Reexecutar |
| --- | --- |
| `description` do `SKILL.md` | Cenários de ativação (3, 9, 10, 13, 14) |
| Fluxo do `SKILL.md` | Todos os cenários |
| `references/audit-criteria.md` ou `research-and-validation.md` | Cenários de segurança e execução afetados |
| `references/colecoes-e-unificacao.md` | 11, 12 e 21 |
| Fixtures ou `expectations` | Os cenários alterados, com recalibração da linha de base |
| Somente `scripts/`, `README.md`, `CHANGELOG.md` | Nenhum cenário; validação estrutural |

## Critérios para publicar a primeira versão (0.1.0)

Todos devem ser verdadeiros no commit que receberá a tag:

- [ ] `python3 scripts/validate.py` sem erros e testes passando.
- [ ] Workflow `validate` verde no commit (conferir na aba Actions).
- [ ] Os sete cenários críticos (2, 5, 8, 15, 16, 17 e 18) executados com e sem a skill, **sem nenhuma falha crítica** (lista em `evals/RESULTS.md`).
- [ ] Cenários de ativação (3, 9, 10, 13, 14) repetidos ao menos 3 vezes cada. O 3 é um valor inicial do protocolo, a recalibrar após a primeira linha de base.
- [ ] Demais cenários executados com e sem a skill e registrados.
- [ ] Cada linha de `evals/RESULTS.md` cita host, modelo, data e hash do commit.
- [ ] Ao menos um host com instalação, descoberta e invocação testadas e registradas na tabela "Hosts validados" do README. Hosts não testados continuam declarados como tal.
- [ ] Licença definida e arquivo `LICENSE` presente.
- [ ] Fontes externas citadas como evidência foram abertas, ou o relatório declara cada pendência.
- [ ] `CHANGELOG.md`: a seção "Não publicado" vira a versão com data e as limitações da versão.

## Passos

1. Abrir PR com o checklist de `.github/pull_request_template.md`.
2. Conferir o CI e os registros de `evals/RESULTS.md` do commit final.
3. Fazer merge somente com os checks `structure` verdes. Para tornar isso obrigatório, exigir esses checks na proteção de branch do GitHub (configuração do repositório, não verificada).
4. Atualizar `CHANGELOG.md`, criar a tag `vX.Y.Z` no commit com CI verde e publicar a release com as limitações da versão.

Uma mudança está "pronta para produção" apenas quando está numa versão com tag. Merge no `main` não é publicação.

## Bloqueios

Qualquer falha crítica, erro estrutural ou ausência de registro dos cenários afetados bloqueia a tag. Não há exceção por média de outras dimensões.
