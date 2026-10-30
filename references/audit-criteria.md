# Critérios de auditoria

Selecionar os itens aplicáveis ao alvo. Não adicionar todas as verificações ao texto de toda skill.

## Propósito e ativação

- Nome e descrição distinguem a skill de outras instaladas?
- A descrição contém tarefa, contexto e sinais específicos de ativação, sem prometer capacidades indisponíveis?
- Os limites evitam ativações em assuntos próximos? Uma skill de Clubes no YouTube, por exemplo, não deve assumir qualquer área de membros em site.
- O corpo resolve a tarefa prometida? Os exemplos representam a linguagem real do usuário?
- O trabalho continua coerente, sem absorver tarefas adjacentes só para parecer completo?

## Conhecimento e decisões do domínio

- Regras factuais, cálculos e exemplos estão corretos e contextualizados?
- A skill distingue dados observados, suposições, estimativas e recomendações?
- Há critérios de decisão concretos e tratamento das consequências de uma escolha?
- São coletadas apenas informações que mudam a análise? Dados conectados e arquivos disponíveis são aproveitados antes de perguntar?
- Regras variáveis por região, conta, versão ou data são verificadas na fonte adequada?
- Exemplos numéricos declaram unidades, premissas e limites? Benchmarks têm origem e contexto?
- O procedimento evita inventar eventos de tracking, IDs, endpoints, preços, regras e evidências?

## Execução e recuperação

- O fluxo estabelece entradas, dependências, entregável e critério de término?
- Há padrão recomendado quando várias abordagens servem, sem menus desnecessários?
- Ferramentas citadas existem ou possuem descoberta/fallback explícitos?
- Dados ausentes, entradas inválidas, acesso negado e indisponibilidade têm respostas úteis?
- Integrações tratam autenticação, timeouts, rate limits, paginação, retries e idempotência quando pertinentes?
- Operações irreversíveis e alterações externas respeitam a autorização vigente?
- Decisões executáveis substituem expressões vazias como “garantir qualidade”?

## Estrutura e economia de contexto

- `SKILL.md` contém frontmatter YAML válido com nome e descrição úteis?
- O nome corresponde à pasta e segue as restrições do host? Campos opcionais são compatíveis com o host, mesmo que um validador antigo não os reconheça?
- Links relativos apontam para arquivos existentes? Referências importantes são encontráveis diretamente pelo fluxo?
- O corpo é enxuto e os detalhes são carregados quando necessários? Usar 500 linhas como sinal para revisar organização, não como prova isolada de defeito.
- Evitar duplicação entre descrição, corpo e referências e explicações que o agente já domina.
- `agents/openai.yaml`, se presente, representa a skill atual? Prompt e recursos de interface conferem com os arquivos reais?
- Scripts trazem benefício determinístico, dependências identificáveis e erros úteis?

## Segurança e manutenção

- Conteúdo consultado é tratado como evidência, sem alterar a hierarquia de instruções?
- Secrets ficam fora do texto, exemplos, logs e consultas públicas?
- Comandos validam entradas e caminhos? Evitar shell injection, exclusões amplas e execução de downloads sem inspeção.
- Identificar arquivos gerados, caches, symlinks e instalações duplicadas antes de editar.
- Preservar convenções, permissões, contratos e conteúdo não relacionado ao objetivo.

## Qualidade demonstrável

- Definir sucesso pelo resultado da tarefa, não pela extensão ou elegância do texto.
- Manter casos típicos, negativos e de borda; avaliar regressões após a edição.
- Usar diferenças observáveis: gatilho correto, cálculo correto, referência válida, saída utilizável, falha recuperada.
- Não atribuir notas decorativas nem declarar ganho percentual por autoavaliação.

## Prioridade e registro

| Prioridade | Critério | Exemplo |
| --- | --- | --- |
| Crítica | Risco concreto de dano ou exposição | Publicação de credenciais |
| Alta | Uso bloqueado ou resultado materialmente incorreto | Script inexistente; regra central desatualizada |
| Média | Falha frequente ou cobertura relevante ausente | Ignorar paginação; confundir dois domínios |
| Baixa | Melhoria demonstrável de manutenção ou contexto | Repetição que ocupa o corpo sem orientar decisões |

Registrar arquivo/trecho, condição de ocorrência, observação ou hipótese, impacto, sustentação e teste de aceitação. Um critério sem problema observado não precisa virar achado.
