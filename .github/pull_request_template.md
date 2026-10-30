## Resumo

O que muda e por quê.

## Tipo de mudança

- [ ] PATCH: link, typo ou fixture sem efeito no comportamento
- [ ] MINOR: instruções, referências, evals ou critérios que alteram comportamento
- [ ] MAJOR: escopo, nome ou contrato da skill

## Verificação

- [ ] `python3 scripts/validate.py` sem erros
- [ ] `python3 -m unittest discover -s scripts -p "test_*.py"` passando
- [ ] CI `validate` verde neste commit
- [ ] Cenários afetados reexecutados com e sem a skill e registrados em `evals/RESULTS.md` (ver `RELEASING.md`), ou "não aplicável: <motivo>"

## Evidência

Links ou linhas de `evals/RESULTS.md`. Separar o que foi executado do que é walkthrough ou estrutural.

## Riscos e limitações

O que não foi verificado.

## Segurança

- [ ] Nenhuma falha crítica em `evals/RESULTS.md` para os cenários afetados
- [ ] Nenhum secret, credencial ou dado pessoal adicionado
