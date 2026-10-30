# Segurança

## Relatar uma vulnerabilidade

Use "Report a vulnerability" na aba Security do repositório no GitHub (relato privado). Esse recurso depende de estar habilitado nas configurações do repositório pelo mantenedor, o que não foi verificado. Se a opção não aparecer, abra uma issue pedindo um canal privado, sem detalhes exploráveis.

Inclua: arquivo e trecho afetados, condição de ocorrência, impacto e passos para reproduzir, sem credenciais reais.

## O que está no escopo

- Instruções da skill que levem um agente a executar comandos, expor segredos, editar o alvo em auditoria somente leitura ou agir externamente sem autorização.
- `scripts/validate.py`: leitura de arquivos fora do projeto, execução de código do material analisado ou vazamento de conteúdo.
- Fixtures de `evals/files/`: elas contêm instruções maliciosas **de propósito** (exfiltração, injeção, instalação suspeita) para testar o agente. Isso não é vulnerabilidade, desde que permaneçam como texto `.txt` que nada executa.

## Tratamento de segredos

Não coloque credenciais, tokens ou dados pessoais em código, fixtures, logs ou issues. Segredo exposto no histórico deve ser revogado, não apenas removido.
