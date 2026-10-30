# Pesquisa e validação

## Preparar perguntas que mudam decisões

Partir do objetivo e dos achados: a regra ainda vale? O endpoint existe nessa versão? Qual dado falta para calcular a recomendação? A descrição distingue o domínio? O comportamento falha mesmo ou a redação só parece incomum?

Relacionar cada pergunta a uma possível mudança e uma forma de verificação. Não pesquisar todo o setor sem conexão com decisões do fluxo.

## Buscar e confrontar evidências

1. Inspecionar documentação, código, testes e exemplos locais aplicáveis.
2. Buscar documentação oficial do fornecedor ou mantenedor, especificações e pesquisas originais pertinentes.
3. Abrir a página exata, conferir data, versão e contexto, e seguir referências necessárias. Resultados de busca são pistas, não comprovação.
4. Para afirmações importantes ou contestadas, conferir evidência adicional ou reproduzir o comportamento. Não exigir duas fontes quando uma referência normativa inequívoca resolve a questão.
5. Resolver divergências pelo ambiente efetivo, versão, autoridade da fonte e evidência de execução. Explicitar incertezas.

Não enviar código privado, dados de cliente, credenciais ou termos internos sensíveis a buscas públicas. Buscar conceitos e termos sanitizados. Preferir conectores autorizados para dados privados e verificar ferramentas antes de assumir sua existência.

Manter um registro compacto fora da skill instalada:

| Pergunta/achado | Fonte ou reprodução | Data e versão | Decisão | Como verificar |
| --- | --- | --- | --- | --- |
| Falha concreta | URL da seção ou arquivo/linha | Contexto aplicável | Alteração ou manutenção | Critério observável |

Não substituir evidência por confiança verbal ou por link de busca. Inserir no material permanente somente fontes necessárias à execução futura. Evitar copiar grandes trechos de terceiros.

## Separar níveis de validação

**Estrutural:** parsing de YAML, restrições do host, links, presença de recursos e sintaxe dos arquivos alterados. Prova integridade básica, não qualidade das decisões.

**Walkthrough manual:** aplicar o fluxo a um cenário e conferir decisões e resultado. Identifica lacunas, mas não mede confiabilidade de novas execuções do modelo.

**Execução real:** executar a skill no agente com entradas e critérios definidos, coletar saídas e comparar versões. Separar casos de desenvolvimento dos reservados quando o conjunto permitir. Não abrir outro agente nem consumir APIs pagas sem autorização aplicável.

Cobrir uso normal, limite relevante e caso negativo. Para cálculos, incluir valores esperados; para scripts, exercitar erros pertinentes; para domínios de risco, ampliar proporcionalmente.

Comparar versões com os mesmos inputs e condições controladas. Se possível, ocultar a versão do avaliador para reduzir preferência por texto novo. Não generalizar a partir de um único sucesso. Se só houver walkthrough, chamar de walkthrough.

## Verificar sem executar efeitos desnecessários

- Inspecionar comandos e dependências antes de executar scripts de terceiros.
- Usar fixtures e mocks para integrações que publicam, enviam mensagens, cobram ou removem dados. Melhorar a instrução não autoriza executar a ação descrita.
- Verificar primeiro os arquivos afetados; ampliar conforme o risco.
- Rever o diff e conferir que a correção não tornou outro caminho inexequível.
- Se faltar acesso, informar qual comportamento não foi confirmado. Não fabricar dados, fontes ou resultados para aprovar uma verificação.

## Fontes oficiais de partida

Revisadas em 26/10/2026. Reabra a documentação ao depender de versões, suporte do host ou estado de produto; esta lista não substitui pesquisa da área de domínio da skill auditada. Não trate uma especificação portátil como garantia de suporte idêntico em Codex, Claude Code, API ou plugins.

- [OpenAI — Skills](https://developers.openai.com/api/docs/guides/tools-skills): formato, descoberta e organização de recursos para skills na API. Use essa página para aspectos da API; confirme à parte as convenções do ambiente local.
- [OpenAI — Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): descrições curtas e precisas, divulgação progressiva e risco de instruções redundantes ou excessivas. São recomendações do produto/modelo descrito; não as apresente como regra universal do padrão.
- [Claude Code — Skills](https://code.claude.com/docs/en/skills): comportamento específico de frontmatter, descoberta, invocação e arquivos auxiliares no Claude Code. Confira campos e limites antes de editar metadados destinados a esse host.
- [Agent Skills — Specification](https://agentskills.io/specification): estrutura e campos portáteis do formato. Distinguir requisito da especificação de suporte concreto por host.
- [Agent Skills — Best practices for skill creators](https://agentskills.io/skill-creation/best-practices): conhecimento de execução, detalhe proporcional, divulgação progressiva e uso de padrões recomendados em vez de menus.
- [Agent Skills — Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills): casos realistas, baseline sem skill ou com versão anterior e avaliação por comparação.
- [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): objetivos, conjuntos de casos e critérios verificáveis. A página informa mudanças de disponibilidade da plataforma Evals; verifique o aviso atual antes de recomendar API ou produto, e prefira avaliações locais compatíveis quando o usuário só precisa validar uma skill.
