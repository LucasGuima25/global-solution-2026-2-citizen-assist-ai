# Auditoria dos critérios - 18/11/2026

**Conclusão:** os requisitos técnicos e documentais verificáveis no PDF fornecido estão atendidos após as correções descritas abaixo. O repositório GitHub público foi criado e o TXT local com os dois links reais foi preparado em 18/11/2026. **Permanece pendente somente enviar o TXT à FIAP ON e confirmar a submissão.**

A conferência comparou as oito páginas do enunciado com código, dados, documentação e evidências executadas. Também consultou o [modelo da coordenação](https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master). Não atribui nota nem substitui eventuais orientações complementares da turma. As Tabelas 1 e 2 do PDF aparecem sem conteúdo; a verificação usa os requisitos textuais disponíveis.

| Critério do enunciado | Resultado e evidência |
|---|---|
| Protótipo funcional em Python | Atendido: interface de terminal e fluxo real de consulta em `src/sistema.py` |
| Pelo menos 15 registros em 3 temas | Atendido: 15 registros, 5 em cada um dos 3 temas |
| Campos essenciais, fonte e data | Atendido: validação do JSON, fontes oficiais e data em cada registro; referências em `fontes.md` |
| Leitura de arquivo e atualização dos dados | Atendido: JSON externo e teste de inclusão de orientação sem reescrever a busca |
| Arquivo ausente, vazio e inconsistente | Atendido: mensagens e testes de regressão |
| Listas, dicionários e recuperação de informações | Atendido: lista de registros, índices por ID/tema e busca lexical explicada |
| Hierarquia/grafo e navegação entre 3 assuntos | Atendido: grafo de temas e relações entre registros; percurso real no roteiro U02 |
| Pergunta ou seleção de assunto | Atendido: pergunta livre e menus de temas/assuntos |
| Múltiplas correspondências e limites | Atendido: seleção de candidatos, recusa por correspondência insuficiente e alternativas de consulta |
| Dois modelos e comparação justificada | Atendido: A direto, B com passos; mesma amostra, respostas registradas, análise estrutural e escolha de B |
| Fonte, aviso e informação não oficial | Atendido: formatadores preservam a orientação, URL, data e aviso; sem geração de fatos por modelo externo |
| Entrada vazia, opção inválida e dúvida fora da base | Atendido: testes e mensagens do menu; ação inversa e número longo também cobertos |
| Pelo menos 12 perguntas e 3 situações de limitação | Atendido: 26 casos, sendo 25 perguntas não vazias, com diretas, reformulações, fora do escopo, ambiguidades e vazio |
| Esperado, obtido, acerto/erro e tempo | Atendido: `resultados/testes.csv`, com 52 execuções A/B sobre os mesmos 26 casos |
| Taxa de acerto e tempo médio | Atendido: 26/26 por modelo; A 2,888 ms e B 2,889 ms nesta execução; fórmulas e limites documentados |
| Facilidade de uso com participante ou roteiro | Atendido pela alternativa de roteiro: 6/6 tarefas reais do menu, transcrições, dificuldades e resultados; sem participante humano alegado |
| Limitações e pelo menos 2 melhorias | Atendido: amostra/vocabulário, atualização das fontes e avaliação com usuários descritos em `avaliacao.md` |
| README completo | Atendido: Grupo 26, nome/RM, problema, público, temas, base, busca, modelos, testes, execução, exemplo literal com fonte, cuidados, vídeo e conclusões |
| Uso de IA e validação crítica | Atendido documentalmente em `uso_ia.md`; o integrante deve compreender e justificar o funcionamento na apresentação |
| Vídeo YouTube Não Listado | Atendido quanto ao acesso e à visibilidade: [vídeo informado](https://youtu.be/OILxfc0eIcc), aberto sem autenticação e identificado como Não Listado em 18/11/2026 |
| Repositório GitHub público e organização final | [Repositório público](https://github.com/LucasGuima25/global-solution-2026-2-citizen-assist-ai) criado em 18/11/2026 para o conteúdo auditado desta atividade; organização descrita no README |
| TXT com somente os dois links na FIAP ON | `entrega.txt` preparado localmente em 18/11/2026 com o repositório público e o vídeo Não Listado; envio e confirmação da submissão na plataforma pendentes |

## Correções realizadas nesta auditoria

1. A busca passou a reconhecer desativar/remover/desabilitar como ação diferente de ativar. Essas consultas não recuperam instruções de ativação quando a base não sustenta a ação pedida.
2. O menu trata uma opção numérica de 5.000 dígitos como inválida, sem encerrar com erro.
3. CID03 passou a informar a exigência de conta gov.br prata ou ouro no Consumidor.gov.br, com fonte principal da própria plataforma e verificação em 18/11/2026. As datas dos outros 14 registros foram preservadas.
4. O README recebeu um exemplo literal de resposta com URL oficial; os tempos da avaliação foram atualizados e a descrição do roteiro evita um tempo de tarefa desatualizado.
5. O campo opcional de turma que estava em branco foi retirado do README: o PDF exige equipe e RMs, já preenchidos. A organização do repositório continua sujeita à orientação da turma.

## Execução final

- `python -m unittest discover -s testes -p "test_*.py" -v`: **12 testes aprovados**.
- `python testes/executar_testes.py`: **26/26 em A e 26/26 em B**; gabarito original preservado.
- `python testes/roteiro_usabilidade.py`: **6/6 tarefas concluídas**.
- O exemplo literal do README foi comparado à saída de `formatar_resposta` e corresponde ao programa.

Os 100% referem-se à amostra e aos critérios de comportamento registrados. Não demonstram compreensão de toda pergunta possível nem constituem uma garantia de nota. A revisão de fonte não é feita automaticamente durante o uso.

O repositório público e o TXT local estão registrados no README e em `entrega.md`. Para uma cópia local, utilizar o ZIP atualizado; a pasta extraída anteriormente pode conter código e documentação anteriores às correções desta auditoria. Nenhuma submissão à FIAP ON foi declarada como realizada.
