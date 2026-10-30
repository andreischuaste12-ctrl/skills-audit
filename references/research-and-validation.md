# Pesquisa e validação

## Preparar perguntas que mudam decisões

Partir do objetivo e dos achados: a regra ainda vale? O endpoint existe nessa versão? Qual dado falta para calcular a recomendação? A descrição distingue o domínio? O comportamento falha mesmo ou a redação só parece incomum?

Relacionar cada pergunta a uma possível mudança e uma forma de verificação. Não pesquisar todo o setor sem conexão com decisões do fluxo.

## Quando pesquisar e até onde

- **Dispensam busca externa:** link quebrado, contradição interna, instrução insegura, frontmatter inválido e qualquer defeito comprovável no próprio arquivo.
- **Exigem busca externa:** regra de plataforma, versão ou assinatura de API, política de região, limite ou campo específico de host, e qualquer afirmação factual que a skill auditada faça sobre o mundo.
- **Limite padrão:** no máximo uma pergunta verificável por achado que dependa de fonte externa, e uma fonte primária por pergunta. Ampliar só quando a fonte for ambígua, estiver desatualizada ou divergir de outra fonte primária, e registrar o motivo da ampliação.
- **Parada:** encerrar quando cada decisão material tiver fonte ou reprodução e cada incerteza restante estiver registrada como pendente.

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

Revisadas em 26/10/2026. Gatilho de revisão: reconferir a lista a cada 90 dias ou antes, quando um host mudar de versão. Reabra a documentação ao depender de versões, suporte do host ou estado de produto; esta lista não substitui pesquisa da área de domínio da skill auditada. Não trate uma especificação portátil como garantia de suporte idêntico em Codex, Claude Code, API ou plugins.

Estar nesta lista não significa que a fonte foi consultada em uma auditoria: cite uma fonte como consultada apenas se a página foi aberta naquela execução. Se uma fonte não puder ser acessada, registre isso no relatório e mantenha a decisão como pendente.

| Fonte | Tipo | Para que serve | Conferência registrada |
| --- | --- | --- | --- |
| [Agent Skills: Specification](https://agentskills.io/specification) | Normativa (formato portátil) | Estrutura e campos portáteis. Distinguir requisito da especificação de suporte concreto por host. | Não acessada em 30/10/2026 (host fora da rede liberada). |
| [Claude Code: Skills](https://code.claude.com/docs/en/skills) | Documentação de host | Frontmatter, descoberta, invocação e arquivos auxiliares no Claude Code. | Aberta em 30/10/2026: `description` e `when_to_use` somam até 1.536 caracteres na listagem; `name` não precisa coincidir com a pasta; campos desconhecidos são ignorados. Em claude.ai e na Skills API, só `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools` são aceitos. Parte final da página não lida. |
| [OpenAI: Skills](https://developers.openai.com/api/docs/guides/tools-skills) | Documentação de plataforma | Formato, descoberta e organização de recursos para skills na API. Confirme à parte as convenções do ambiente local. | Não acessada em 30/10/2026 (host fora da rede liberada). |
| [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) | Recomendação | Conhecimento de execução, detalhe proporcional, divulgação progressiva e padrões recomendados em vez de menus. | Não acessada em 30/10/2026 (host fora da rede liberada). |
| [Agent Skills: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) | Recomendação | Casos realistas, baseline sem skill ou com versão anterior e avaliação por comparação. | Não acessada em 30/10/2026 (host fora da rede liberada). |
| [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Recomendação do produto/modelo descrito (não regra universal) | Descrições curtas e precisas, divulgação progressiva e risco de instruções redundantes ou excessivas. | Não acessada em 30/10/2026 (host fora da rede liberada). Conferir a existência da página antes de depender dela. |
| [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Recomendação / documentação de plataforma | Objetivos, conjuntos de casos e critérios verificáveis. A página informa mudanças de disponibilidade da plataforma Evals; verifique o aviso atual antes de recomendar API ou produto e prefira avaliações locais compatíveis quando o usuário só precisa validar uma skill. | Não acessada em 30/10/2026 (host fora da rede liberada). |

### Manutenção das fontes

- Ao incluir uma fonte, registrar o motivo de uso, o tipo (normativa, documentação de host, recomendação) e a data da conferência.
- Ao depender de uma fonte em uma auditoria, reabrir a página e anotar data e versão quando a informação variar por produto ou host.
- Separar regra normativa de recomendação ao justificar uma mudança. Recomendação sustenta melhoria opcional, não defeito.
- Um verificador automático de links detecta URL inválida, mas não prova que o conteúdo é atual nem aplicável.
