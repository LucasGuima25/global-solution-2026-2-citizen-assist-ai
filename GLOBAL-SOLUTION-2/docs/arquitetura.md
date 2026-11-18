# Organização, busca e navegação

## Fluxo e responsabilidades

1. `src/base.py` lê o JSON e valida o conteúdo antes de iniciar a consulta.
2. `criar_indices` mantém um dicionário por ID e listas agrupadas por tema.
3. `src/sistema.py` recebe pergunta ou escolha de menu.
4. `src/busca.py` compara a pergunta à base e devolve encontrado, ambíguo, sem resposta ou inválido.
5. `src/respostas.py` aplica A/B exclusivamente ao registro selecionado.
6. A interface oferece assuntos relacionados ou temas alternativos.

O programa mantém os registros em memória durante a sessão. Para revisar uma orientação, alterar o JSON e reiniciar a aplicação. Não existe banco de dados, gravação de consultas, treinamento nem requisição HTTP no fluxo de uso.

## Dados e validação

A raiz do arquivo é uma lista de objetos. Os campos obrigatórios são `id`, `tema`, `titulo`, `pergunta`, `palavras_chave`, `orientacao`, `passos`, `fonte`, `verificado_em`, `aviso` e `relacionados`. `fonte` contém `titulo` e `url`; palavras-chave, passos e relações são listas.

São rejeitados arquivo ausente/ilegível, texto vazio, JSON malformado, raiz indevida, campos vazios ou de tipo incorreto, IDs duplicados, tema desconhecido, data fora do formato ISO, fonte não HTTPS oficial e relações duplicadas, consigo mesmo ou inexistentes. Os domínios aceitos são `gov.br`, `jus.br`, `leg.br` e seus subdomínios; isso valida o formato e a origem do endereço, sem provar a atualidade ou o conteúdo da página.

O carregador aceita bases menores para permitir manutenção e testes isolados. O requisito acadêmico de 15 registros em 3 temas é conferido no conjunto entregue pelos testes. A data registra quando a orientação foi conferida, não um prazo de validade automática.

## Estratégia de busca

O algoritmo é uma busca lexical sobre apenas 15 registros, adequada ao escopo introdutório. Não interpreta linguagem como um modelo generativo.

1. Normalizar letras maiúsculas/minúsculas, acentos, espaços e pontuação; agrupar `gov.br` como `govbr`.
2. Aplicar equivalências explícitas pequenas, como `esqueci` → `recuperar`, e remover palavras de ligação/pedidos genéricos que não distinguem o assunto.
3. Se a entrada indicar somente um tema amplo, como `documento digital`, devolver os assuntos possíveis para escolha. Entrada vazia é inválida. Solicitações explicitamente não cobertas por fraude/invasão são recusadas.
4. Se houver uma ação reconhecida na pergunta, exigir que a primeira ação também esteja representada no título, pergunta ou palavras-chave do registro. Classes como consultar, criar, recuperar, alterar, solicitar, renovar e desativar evitam confundir acesso digital à CNH com renovação, consulta do CPF com emissão ou desativação com ativação de proteção. `Desativar`, `remover` e `desabilitar` são agrupadas como desativação; sem orientação que sustente a ação, a consulta é recusada.
5. Para cada registro disponível, comparar palavras da pergunta com o corpus formado por título, pergunta, palavras-chave, orientação e passos. Contar a frequência de cada palavra nos registros.
6. Cada palavra compartilhada recebe peso `1 / frequência`; palavras dos campos principais recebem mais um ponto. Somar a cobertura, calculada como palavras compartilhadas / palavras relevantes da pergunta.
7. Considerar candidatos com cobertura de pelo menos 50%. O melhor só pode gerar resposta com cobertura de pelo menos 75% e uma palavra que apareça em no máximo dois registros. Sem isso, informar correspondência insuficiente.
8. Se outros candidatos ficarem a até 0,25 ponto do melhor, pedir esclarecimento; caso contrário, apresentar o registro localizado. Ordenar os empates pelo ID torna o resultado reproduzível.

Os números acima são regras heurísticas do protótipo, **não probabilidades de correção**. Não houve treino estatístico ou conjunto independente de validação. O algoritmo foi refinado durante os testes de desenvolvimento e pode exigir reformulação de uma paráfrase nova. A busca usa conjuntos de palavras; não compreende plenamente negações, contexto longo, ironia ou a intenção de toda pergunta. O menu é uma alternativa explícita quando o texto livre não é suficiente.

O custo é linear no número de registros e no tamanho do texto comparado; não há indexação persistente. Para a base pequena, a simplicidade permite explicar e revisar a comparação. O dicionário por ID oferece acesso direto durante a navegação, enquanto o agrupamento por tema restringe os assuntos apresentados.

## Grafo simples

`GRAFO_TEMAS` conecta os três temas de forma não direcionada: conta gov.br ↔ documentos digitais ↔ serviços ao cidadão, incluindo a ligação conta ↔ serviços. As arestas indicam relações de navegação, não comprovam que todo serviço exija todo documento ou nível de conta.

Além disso, o campo `relacionados` representa arestas direcionadas entre orientações. Por exemplo, GOV01 leva a GOV02, e GOV02 leva a GOV04. A interface permite percorrer esses três assuntos e voltar. O percurso usa repetição, evitando uma pilha recursiva a cada nova escolha.

## Atualização

Para incluir um registro dentro dos temas existentes, preencher o schema, usar um ID único e apontar relações válidas. Conferir a fonte antes de gravar a data, executar os testes e acrescentar perguntas pertinentes. A validação estrutural pode aceitar um texto factualmente incorreto; por isso a revisão da fonte é responsabilidade de quem mantém a base.
