# Correspondência entre enunciado e evidências

Referência: Global Solution 2026.2, CitizenTech / Citizen Assist AI, PDF fornecido pelo estudante. A tabela indica onde conferir a implementação e seus resultados; não representa uma nota atribuída pela banca.

| Exigência | Evidência |
|---|---|
| Pelo menos 15 orientações em pelo menos 3 temas | `dados/base_conhecimento.json` e `docs/fontes.md` |
| Identificador, tema, pergunta/palavras-chave, orientação, referência e data | Campos de cada registro; validação em `src/base.py` |
| Leitura de JSON/TXT/CSV e base atualizável | JSON externo, carregado por `carregar_base`; inclusão de conteúdo não exige alterar busca/formatação |
| Arquivo ausente, vazio e inconsistente | Validações de `src/base.py` e testes em `testes/test_sistema.py` |
| Uso de listas e dicionários; busca por pergunta/assunto | Índices em `src/base.py`, busca em `src/busca.py`, navegação em `src/sistema.py` |
| Hierarquia/grafo e navegação entre 3 assuntos relacionados | `GRAFO_TEMAS` e campo `relacionados`; explicação no README |
| Explicar comparação e múltiplas correspondências | `docs/arquitetura.md` e fluxo de seleção de candidatos no terminal |
| Dois modelos de instrução/resposta e comparação | `src/respostas.py`, `docs/modelos_resposta.md`, `resultados/comparacao_modelos.csv` |
| Resposta com fonte e limites, sem inventar orientações | Formatação exclusivamente de conteúdo da base, referências e avisos; recusa de consultas sem sustentação |
| Consulta por menu e texto | Menu principal e opção de explorar temas; modo `--pergunta` para demonstração reproduzível |
| Entrada vazia, opção inexistente, ambiguidade e ausência de resposta | Testes e roteiro de tarefas; mensagens e sugestões da interface |
| Pelo menos 12 perguntas e 3 situações de limitação | `testes/casos_teste.json` e registro de resultados |
| Esperado, obtido, acerto/erro e tempo | `resultados/testes.csv` |
| Taxa de acerto e medida de tempo | `resultados/indicadores.json` e interpretação em `docs/avaliacao.md` |
| Teste de facilidade de uso com usuário ou roteiro | `testes/roteiro_usabilidade.py`, resultados/transcrições e `docs/avaliacao.md` |
| Interpretar limitações e propor 2 melhorias | `docs/avaliacao.md` |
| README com equipe/RMs, execução, problema e evidências | `README.md`; Grupo 26, LUIZ LUCAS GUIMARAES, RM574169, exemplo literal com fonte e link do vídeo registrados |
| Registrar apoio de IA e validação crítica | `docs/uso_ia.md` |
| Repositório público e vídeo Não Listado | [Repositório público](https://github.com/LucasGuima25/global-solution-2026-2-citizen-assist-ai) criado em 18/11/2026; [vídeo](https://youtu.be/OILxfc0eIcc) acessível sem autenticação e identificado como Não Listado na mesma data |
| TXT com apenas os 2 links na FIAP ON | Arquivo local `entrega.txt` preparado em 18/11/2026 com as duas URLs reais; envio e confirmação da submissão na FIAP ON permanecem pendentes |

Uma interface de terminal atende ao enunciado. O escopo usa Python e biblioteca padrão, sem exigir interface web, APIs pagas, LangChain, n8n ou treinamento de modelo.

As Tabelas 1 e 2 do PDF aparecem sem conteúdo na renderização. A estrutura interna foi organizada a partir das exigências textuais e do [modelo indicado](https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master), preservando `src/sistema.py` e `docs/uso_ia.md`. A localização da pasta no portfólio deve seguir a turma do estudante.
