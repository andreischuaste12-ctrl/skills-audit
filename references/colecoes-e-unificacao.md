# Auditoria de coleções e unificação

Carregue este protocolo somente quando o usuário indicar mais de uma skill, pedir análise de um diretório/pacote ou perguntar o que deve ser unificado. Não aplique à revisão isolada de uma skill.

## 1. Inventariar o escopo

Inspecione apenas o conjunto indicado e dependências diretamente referenciadas. Para cada skill, registre:

| Campo | O que verificar |
|---|---|
| Identidade e origem | Nome, caminho, proprietário, fonte editável, instalação, cache ou vínculo externo |
| Propósito | Tarefa, público, contexto, entrada e entrega prometida |
| Ativação | O que deve disparar e o que deve ficar fora |
| Procedimento | Decisões, ferramentas, critérios de término e recuperação |
| Ativos | Referências, scripts, templates, dependências, avaliações e integrações |
| Uso cruzado | Skills chamadas, citadas, duplicadas ou necessárias como encaminhamento |

Não trate cópias de auditoria, exemplos, backups, caches ou diretórios de dependências como instalações ativas. Resolva junctions/symlinks e origem antes de recomendar edição, remoção ou instalação.

## 2. Medir sobreposição por fluxo

Compare objetivo do usuário, entradas, decisões, entregável, ferramentas e critérios de sucesso. Use palavras-chave parecidas apenas para localizar candidatas; elas não provam redundância.

Classifique cada relação como:

- **Complementar:** uma skill entrega entrada necessária à outra, mas têm tarefas e entregas diferentes. Preserve ambas e documente o encaminhamento.
- **Sobreposição parcial:** compartilham uma etapa, repertório ou ferramenta, mas têm resultados distintos. Preserve a skill especializada; extraia ou referencie somente o procedimento comum se isso reduzir manutenção sem ocultar a fronteira.
- **Duplicidade funcional:** duas skills atendem à mesma intenção, com entradas, decisões e entregáveis essencialmente iguais. Avalie unificação e escolha uma origem editável canônica.
- **Conflito de roteamento:** descrições fazem skills diferentes ativarem para o mesmo pedido ou nenhuma cobre uma tarefa importante. Corrija descrições, limites e encaminhamentos antes de considerar unificação.

## 3. Decidir o destino sem ambiguidade

Para cada skill, escolha uma ação e justifique-a por evidência:

| Ação | Critério de decisão |
|---|---|
| **Manter** | Tem propósito e resultado próprios; não há defeito material demonstrado. |
| **Melhorar** | O propósito continua válido, mas há falha concreta em gatilho, instrução, evidência, ferramenta, recuperação ou validação. |
| **Unificar** | Mesmo trabalho principal, entradas e entregáveis compatíveis; a união diminui conflito ou duplicação sem perder cobertura distinta. |
| **Dividir** | Uma skill mistura intenções com entradas, decisões, ferramentas ou saídas incompatíveis e isso prejudica ativação ou execução. |
| **Encaminhar/referenciar** | Uma skill é especialista ou dependência complementar. Indique condição e destino do encaminhamento sem copiar seu procedimento inteiro. |
| **Retirar de uso** | Skill sem usuário/caso válido, substituída ou inviável. Proponha desativação; não apague nem desinstale sem autorização explícita. |

**Não unifique** apenas para reduzir contagem, por área ampla compartilhada ou por usar as mesmas ferramentas. Unifique somente quando o fluxo real é comum e uma única descrição consegue selecionar corretamente os casos positivos e rejeitar os negativos. Preserve diferenças que mudam decisão, risco, fonte, plataforma, autorização ou formato de saída.

## 4. Planejar e aplicar uma unificação

Antes de editar, monte um mapa de migração: skill de origem → conteúdo/ativos preservados → destino → referências e invocações a atualizar. Em seguida:

1. Escolha a fonte canônica pelo contexto do usuário, qualidade, compatibilidade e origem editável; não instale uma terceira cópia.
2. Combine apenas instruções comprovadamente comuns. Mantenha regras específicas em módulos carregados sob condição explícita.
3. Atualize nome, descrição, frontmatter, prompt da interface, avaliações, links internos, referências de outras skills e vínculos de descoberta que estejam no escopo autorizado.
4. Preserve nome de comando, pacote ou endpoint externo quando renomear quebrar a integração. A identidade pessoal da skill pode usar o sufixo `-konvert`, conforme as instruções globais.
5. Não apague os originais durante a unificação. Deixe-os intactos até que o usuário autorize a retirada e até que referências, instalação e consumidores tenham sido conferidos.

Se a única melhoria segura for corrigir roteamento, não force uma unificação: aplique a correção mínima de descrições, limites e referências.

## 5. Verificar a coleção

Monte casos de avaliação a partir dos conflitos observados, não de categorias abstratas:

- um pedido típico que deve ativar cada skill mantida;
- um pedido semelhante que deve ser recusado ou encaminhado a outra skill;
- pelo menos um par de tarefas que parecia sobreposto, mas precisa continuar distinto;
- após unificação, um caso coberto por cada skill de origem e um caso negativo de cada fronteira importante.

Verifique nome e diretório, metadados, links locais, referências cruzadas, ativos preservados e descoberta nos hosts autorizados. Compare a linha de base e a versão revisada nos mesmos casos. Se não houver execução real do agente, reporte somente walkthrough e checagens estruturais.

## 6. Relatar a decisão

Entregue uma linha por skill, inclusive as que ficam como estão:

| Skill | Decisão | Evidência/limite observado | Alteração aplicada ou proposta | Verificação |
|---|---|---|---|---|

Priorize bloqueios, erros factuais ou de segurança, conflito de ativação, cobertura insuficiente e manutenção. Separe ação executada de recomendação pendente e explique qualquer fonte que não pôde ser alterada.
