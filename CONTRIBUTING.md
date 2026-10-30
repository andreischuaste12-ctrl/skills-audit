# Contribuindo

Contribuições são bem-vindas. Idioma dos documentos e das mensagens: português do Brasil, com termos técnicos em inglês.

## Antes de abrir um PR

```bash
pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p "test_*.py"
```

Os dois comandos precisam passar. O CI roda a mesma verificação em Python 3.11, 3.12 e 3.13.

## Regras

- Preencha o checklist de `.github/pull_request_template.md`.
- Mudança que altera o comportamento da skill (descrição, fluxo, referências, fixtures ou critérios) exige reexecutar os cenários afetados, com e sem a skill, e registrar em `evals/RESULTS.md`. A tabela de `RELEASING.md` diz quais.
- Não declare melhoria, ganho percentual ou compatibilidade de host sem execução registrada.
- Fixtures de `evals/files/` usam extensão `.txt` e nunca o nome `SKILL.md`, para não serem descobertas como skills. Nada de credenciais reais: use valores obviamente falsos e domínios `.invalid`.
- O validador rejeita symlinks e caminhos fora de `evals/files`. Não tente contornar essas regras.
- Não adicione dependências de runtime. A única dependência de desenvolvimento é a de `requirements-dev.txt`.

## Segurança

Para vulnerabilidades, veja `SECURITY.md`; não abra issue pública com detalhes exploráveis.
