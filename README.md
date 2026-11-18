# Citizen Assist AI

Atividade organizada na pasta [GLOBAL-SOLUTION-2](https://github.com/LucasGuima25/global-solution-2026-2-citizen-assist-ai/tree/main/GLOBAL-SOLUTION-2). Abra o terminal nessa pasta para executar os comandos abaixo.

Global Solution 2026.2 - CitizenTech - FIAP.

Assistente introdutório em Python para organizar orientações cidadãs, apresentar suas referências e reconhecer quando não há informação suficiente. O projeto usa somente a biblioteca padrão, uma base JSON local e interface de terminal.

## Identificação da entrega

- **Nome da equipe:** Grupo 26.
- **Integrante:** LUIZ LUCAS GUIMARAES — RM574169.
- **Repositório GitHub público:** [Código e documentação](https://github.com/LucasGuima25/global-solution-2026-2-citizen-assist-ai).
- **Vídeo no YouTube (Não Listado):** [Assistir à apresentação](https://youtu.be/OILxfc0eIcc).

Identificação e link do vídeo informados pelo integrante. O vídeo foi aberto sem autenticação e identificado como **Não Listado** em 18/11/2026. O repositório público foi criado e o arquivo local `entrega.txt`, com os dois links, foi preparado em 18/11/2026.

## Problema, público e escopo

Pessoas que procuram documentos e serviços digitais encontram informações dispersas e nem sempre identificam o canal adequado. O assistente oferece orientações gerais em linguagem simples, com fonte oficial, data de verificação e aviso sobre limites.

A base contém **15 orientações**, distribuídas em **3 temas**, com 5 registros por tema:

| Tema | Assuntos |
|---|---|
| Conta gov.br | Criação, recuperação de senha, níveis, duas etapas e atualização de contato |
| Documentos digitais | Carteira de Trabalho Digital, CNH digital, CRLV-e, CIN digital e e-Título |
| Serviços ao cidadão | Ouvidoria, acesso à informação, Consumidor.gov.br, situação do CPF e localização de CRAS |

O público beneficiado são pessoas que precisam localizar orientações e canais oficiais brasileiros. O aplicativo não presta atendimento oficial, não executa serviços e não consulta a situação individual de ninguém. Os registros identificam a abrangência e as condições de cada orientação. A verificação inicial ocorreu em **10/11/2026**; CID03 foi atualizado em **18/11/2026**. Cada registro informa sua data, e as referências estão em [fontes e limites](GLOBAL-SOLUTION-2/docs/fontes.md).

## Como executar

Requisito: **Python 3.10 ou superior** em um terminal com suporte a UTF-8. Não é necessário instalar pacotes com pip, obter chaves ou configurar serviços externos.

Abra o terminal na pasta `GLOBAL-SOLUTION-2` e execute:

```bash
python src/sistema.py
```

O menu permite perguntar, explorar temas/assuntos, trocar o modelo A/B e consultar os limites. `0` volta ao menu anterior ou encerra a aplicação. Após uma resposta, é possível seguir os assuntos relacionados. Entradas inválidas mostram uma mensagem e permitem tentar novamente.

Para uma consulta única, útil em demonstrações:

```bash
python src/sistema.py --pergunta "Como recuperar a senha da conta gov.br?"
python src/sistema.py --pergunta "Como acessar a CNH digital?" --modelo A
python src/sistema.py --pergunta "Como acessar a CNH digital?" --modelo B
```

Os argumentos `--tema conta_govbr`, `--tema documentos` e `--tema servicos_cidadao` restringem uma consulta ao tema escolhido. `--base caminho.json` permite conferir outro arquivo. Os caminhos padrão são calculados a partir do script, sem depender da pasta corrente.

## Organização e funcionamento

```text
src/          leitura/validação, busca, respostas e interface textual
dados/        15 orientações verificadas em JSON
testes/       gabarito, avaliação A/B, regressões e roteiro de tarefas
resultados/   CSVs, indicadores e transcrições reais do roteiro
docs/         fontes, arquitetura, modelos, avaliação, uso de IA e entrega
```

Cada registro possui identificador, tema, título, pergunta, palavras-chave, orientação, passos, referência, data, aviso e assuntos relacionados. O carregador valida campos/tipos, IDs duplicados, fontes HTTPS oficiais, datas e relações inexistentes. Arquivos ausentes, vazios, ilegíveis ou com JSON inconsistente geram mensagens compreensíveis.

Listas organizam os registros. Dicionários permitem acesso por identificador e agrupamento por tema. A busca compara palavras normalizadas e trata correspondências fracas ou próximas de forma conservadora, sem usar um modelo generativo. A estratégia, seus critérios e seus limites estão em [arquitetura](GLOBAL-SOLUTION-2/docs/arquitetura.md).

Os três temas formam um grafo simples: a conta dá acesso a documentos e serviços; documentos podem ser necessários em serviços. Cada registro também possui arestas explícitas em `relacionados`. Um percurso disponível é **criar conta (GOV01) → recuperar senha (GOV02) → duas etapas (GOV04)**. O usuário escolhe se quer continuar e pode voltar a qualquer momento.

Para acrescentar orientações, edite `dados/base_conhecimento.json`, preencha todos os campos e referências, associe um dos temas existentes e execute os testes. O código de busca e resposta não precisa ser reescrito. Novos temas exigem atualizar o mapa de temas e suas relações em `src/base.py`.

## Respostas, fontes e limites

O modelo **A** apresenta a orientação diretamente. O modelo **B**, padrão, acrescenta os passos cadastrados em uma lista numerada. Ambos preservam a mesma orientação, fonte, data e aviso. As instruções e a comparação estão em [modelos de resposta](GLOBAL-SOLUTION-2/docs/modelos_resposta.md).

Exemplos de comportamento:

| Entrada | Comportamento esperado |
|---|---|
| `Como recuperar a senha da conta gov.br?` | Localiza GOV02, mostra o procedimento, o link oficial e o aviso para não fornecer senhas ao assistente |
| `documento digital` | Apresenta mais de um documento e pede escolha, sem adivinhar o assunto |
| `Como emitir meu passaporte?` | Informa que não há orientação suficiente na base e oferece os temas disponíveis |
| Pergunta vazia ou opção de menu inexistente | Explica como corrigir a entrada |

Exemplo de resposta do modelo A à pergunta `Como acessar a Carteira de Trabalho Digital?`:

```text
DOC01 - Acessar a Carteira de Trabalho Digital

A Carteira de Trabalho Digital pode ser acessada pelo aplicativo oficial ou pelo serviço web indicado no portal gov.br. É necessário estar inscrito no CPF e ter uma conta autenticada gov.br. O serviço é gratuito.

Fonte: Ministério do Trabalho e Emprego - Obter a Carteira de Trabalho
https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
Verificado em: 2026-11-10
Atenção: Este assistente não consulta vínculos de trabalho. Para dificuldade de acesso ou dados, utilize o atendimento indicado pelo Ministério do Trabalho e Emprego.
Protótipo acadêmico. Este assistente não é um canal oficial de atendimento.
```

As saídas completas, incluindo referências reais, podem ser reproduzidas pelos comandos acima e estão registradas em `resultados/testes.csv` e `resultados/transcricoes/`.

Não são pedidos CPF, senha, endereço ou documentos pessoais. Perguntas feitas no uso normal não são gravadas nem enviadas à internet. Os arquivos de evidência contêm somente entradas fictícias, definidas nos testes. A interface usa texto, navegação por teclado, opções numeradas e mensagens simples; não exige imagens, cores, áudio ou mouse para operar.

## Testes e avaliação

O gabarito contém **26 casos distintos**, incluindo perguntas diretas, reformulações, assuntos fora da base, ambiguidades e entrada vazia. Cada caso é aplicado aos dois modelos; a avaliação registra esperado, obtido, acerto/erro, referência e tempo de busca/formatação. Há também testes de regressão para leitura de arquivos, atualização por dados e limites da busca.

```bash
python -m unittest discover -s testes -p "test_*.py" -v
python testes/executar_testes.py
python testes/roteiro_usabilidade.py
```

Os dois últimos comandos atualizam os resultados locais. O roteiro percorre seis tarefas do menu real, salva transcrições e registra conclusão/dificuldades. Não houve teste com participante humano; foi usada a alternativa de roteiro de tarefas permitida pelo enunciado. A taxa de conclusão das tarefas não mede satisfação ou tempo de leitura humana.

Na auditoria registrada em 18/11/2026, os **12 testes de regressão passaram**. A e B acertaram **26/26 casos cada** (100% nesta amostra), com médias de **2,888 ms** e **2,889 ms**, respectivamente. O roteiro concluiu **6/6 tarefas**. A diferença de tempo é pequena e não justifica escolher um modelo por velocidade; B foi escolhido por explicitar os passos, preservando fonte e limites. A amostra foi usada no desenvolvimento e não é uma prova independente de generalização.

Os valores medidos, o denominador, a comparação A/B e a interpretação estão em [avaliação](GLOBAL-SOLUTION-2/docs/avaliacao.md). Uma recusa ou solicitação de esclarecimento correta conta como acerto de comportamento. Acertar esta amostra não comprova que qualquer pergunta futura será respondida corretamente. As checagens automáticas de preservação de texto não provam, sozinhas, atualização factual de uma página.

## Conclusões e melhorias

O projeto demonstra leitura de arquivos, listas/dicionários, validações, busca lexical, grafo simples, regras de resposta e avaliação reproduzível. A organização permite revisar o conteúdo sem alterar a lógica central.

As principais limitações são a base pequena e estática, a busca sensível às palavras usadas e a avaliação sem usuários reais. Duas melhorias prioritárias são ampliar a amostra de perguntas e os sinônimos com dados de testes reais, e estabelecer revisão periódica das fontes por um responsável. Uma avaliação com usuários do público beneficiado deve verificar se a linguagem e o percurso de navegação são compreensíveis.

O apoio de IA utilizado na elaboração está registrado em [uso de IA](GLOBAL-SOLUTION-2/docs/uso_ia.md). O protótipo não utiliza APIs de IA, treinamento ou geração de orientações durante a consulta. Os integrantes precisam compreender, revisar e justificar o funcionamento antes da apresentação.

## Evidências e entrega

- [Requisitos e evidências](GLOBAL-SOLUTION-2/docs/requisitos.md)
- [Auditoria dos critérios em 18/11/2026](GLOBAL-SOLUTION-2/docs/auditoria_banca.md)
- [Plano e interpretação da avaliação](GLOBAL-SOLUTION-2/docs/avaliacao.md)
- [Roteiro do vídeo](GLOBAL-SOLUTION-2/docs/roteiro_video.md)
- [Roteiro breve para gravar a apresentação em até 3 minutos](GLOBAL-SOLUTION-2/docs/roteiro_gravacao_3min.md)
- [Passos para publicar e entregar](GLOBAL-SOLUTION-2/docs/entrega.md)

Seguir o [modelo da coordenação](https://github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON/tree/master) e acomodar esta atividade à pasta da turma. O PDF apresenta as Tabelas 1 e 2 sem conteúdo; a organização interna segue as exigências textuais disponíveis.

A entrega final na FIAP ON é um TXT contendo apenas o link real do repositório GitHub público e o link real do vídeo YouTube Não Listado. Os dois links estão registrados acima e no arquivo local [entrega.txt](GLOBAL-SOLUTION-2/entrega.txt), preparado em 18/11/2026. **Permanece pendente enviar esse TXT à FIAP ON e confirmar o registro da submissão.** Conferir prazo e instruções vigentes na plataforma, inclusive orientações da coordenação sobre a turma.
