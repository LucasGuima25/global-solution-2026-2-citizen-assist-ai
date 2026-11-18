# Testes, indicadores e interpretação

## Método e amostra

Avaliação executada em 18/11/2026 com Python 3.12.14 no Windows 11. O conjunto em `testes/casos_teste.json` possui **26 casos distintos**: 15 perguntas diretas, 3 reformulações, 5 perguntas fora do escopo, 2 ambiguidades e 1 entrada vazia. São 25 entradas não vazias, acima das 12 perguntas mínimas, e existem casos explícitos de entrada vazia, ambiguidade e ausência de orientação confiável.

O esperado foi definido pelo assunto e pelo comportamento previsto, antes da execução. O mesmo conjunto foi executado em A e B. Cada resposta localizada é confrontada com o ID e a orientação esperados, além das verificações de fonte, data, aviso e formato. Respostas completas estão em `resultados/testes.csv`; não foram preenchidas saídas ou tempos fictícios.

O gabarito foi utilizado no desenvolvimento e na correção da busca. Portanto, este é um teste de aceitação/regressão, não um conjunto independente para estimar generalização. Na primeira rodada, 23/26 casos acertaram por modelo: surgiram dificuldades com a formulação sobre CIN, localização de CRAS e um falso positivo entre telefone de conta bancária e conta gov.br. A normalização, a cobertura e a compatibilidade da ação foram refinadas mantendo o gabarito original.

## Resultados registrados

| Modelo | Casos corretos / avaliados | Taxa de comportamento correto | Tempo médio |
|---|---|---|---|
| A | 26/26 | 100% | 2,888 ms |
| B | 26/26 | 100% | 2,889 ms |

São 52 execuções ao aplicar dois modelos aos mesmos 26 casos, não 52 perguntas distintas. A taxa por modelo é `26 / 26 × 100`. Uma recusa correta fora do escopo, uma solicitação correta de esclarecimento e o tratamento da entrada vazia contam como acerto de comportamento. A taxa de 100% refere-se somente a esta amostra e a estes critérios.

Nos dois modelos: 15/15 diretas, 3/3 reformulações, 5/5 fora do escopo, 2/2 ambiguidades e 1/1 entrada vazia tiveram o comportamento previsto. Os valores completos, o ambiente e o instante de execução estão em `resultados/indicadores.json`.

O tempo médio é `soma dos tempos / 26`, medido com `perf_counter`, incluindo busca e formatação. Exclui leitura inicial do arquivo, digitação, leitura pelo usuário e serviços externos. A diferença de aproximadamente 0,001 ms entre os modelos nesta execução é pequena e não sustenta conclusão de superioridade de desempenho. A execução dos scripts em outro equipamento produzirá tempos diferentes.

Além da amostra, **12 testes de regressão** passaram: arquivos ausentes/vazios/JSON inválido, registros inconsistentes, mínimos e índices, atualização por dados, entrada vazia, ambiguidade, termos fora do escopo, ações parcialmente relacionadas, normalização, preservação das respostas, ação inversa e opção numérica excessivamente longa. Incluem recusa de renovação de CNH e solicitação de CPF, assuntos não cobertos pelas respectivas orientações digitais/de consulta.

A auditoria de 18/11/2026 identificou e corrigiu dois problemas adicionais: pedir para desativar/remover a verificação em duas etapas podia recuperar a orientação de ativação; uma opção com 5.000 dígitos podia interromper o menu. Os novos testes confirmam a recusa da ação sem orientação correspondente e a recuperação do menu após a opção inválida. O gabarito original de 26 casos foi preservado.

## Facilidade de uso por roteiro

Foi usada a alternativa de **roteiro de tarefas**, com execução automatizada sobre o programa real por subprocesso e entradas fictícias. Não houve participante humano ou entrevista. `testes/roteiro_usabilidade.py` salva resultados em `resultados/usabilidade.csv` e transcrições em `resultados/transcricoes/`.

| Tarefa | Percurso | Resultado |
|---|---|---|
| U01 | Perguntar sobre recuperação de senha e ler fonte/limite | Concluída |
| U02 | Navegar GOV01 → GOV02 → GOV04 | Concluída |
| U03 | Corrigir opção inexistente e pergunta vazia | Concluída |
| U04 | Desambiguar documento digital e selecionar orientação | Concluída |
| U05 | Receber limite para passaporte e localizar temas alternativos | Concluída |
| U06 | Trocar A/B e consultar o mesmo assunto | Concluída |

Taxa de conclusão do roteiro: `6 / 6 × 100 = 100%`. Os tempos de cada tarefa estão registrados em `resultados/usabilidade.csv`, variam entre execuções e incluem inicialização e execução automatizada; não medem esforço, compreensão ou velocidade humana.

**Dificuldades e custos identificados no percurso:** consultas vagas exigem uma escolha adicional; a mesma opção `0` volta apenas um nível por vez, exigindo retornos adicionais até sair; os avisos e referências tornam algumas respostas longas; texto livre com vocabulário novo pode exigir reformulação ou escolha pelo menu. As seis tarefas puderam ser concluídas apesar dessas restrições. A observação é uma análise do percurso e das saídas, não uma opinião coletada de usuários.

## Limitações e melhorias

1. **Vocabulário e amostra:** 15 registros e 26 casos não representam a diversidade de dúvidas. A regra lexical, inclusive a primeira ação reconhecida, não entende plenamente contexto ou negações. Ampliar o conjunto com novas perguntas e paráfrases obtidas em testes reais, mantendo uma amostra futura separada do ajuste do algoritmo.
2. **Atualização:** o programa consulta uma base estática. Estabelecer revisão periódica por responsável, reabrir fontes e alterar a data apenas depois da conferência. Não confundir um domínio oficial válido com prova de atualização factual.
3. **Facilidade de uso:** o roteiro confirma que caminhos previstos funcionam, mas não avalia compreensão ou satisfação. Realizar teste com pessoas do público beneficiado e revisar linguagem, extensão das respostas e necessidade de tantos retornos de menu.

Essas melhorias são propostas futuras. A implementação atual mantém o escopo de Python, arquivos, estruturas, busca, modelos de instrução e avaliação exigido na atividade.

Para reproduzir, executar os três comandos de teste do README. Os scripts regeneram as evidências reais; se os arquivos mudarem, revisar esta interpretação para refletir os novos resultados.
