# Dois modelos de instrução e resposta

Os modelos estão explicitamente definidos em `MODELOS`, em `src/respostas.py`. São regras de apresentação aplicadas por Python, sem chamada a LLM. A ausência de serviço externo é permitida pelo enunciado; elaborar, documentar e comparar os dois modelos continua sendo parte do trabalho.

## Modelo A: resposta direta

**Instrução:** atuar como assistente acadêmico de orientação cidadã; apresentar título e orientação em um parágrafo; identificar fonte, URL, data e aviso; não acrescentar fatos nem alegar atendimento oficial.

**Formato:** identificador/título → orientação → fonte → data → aviso → identificação de protótipo não oficial.

## Modelo B: resumo e passos

**Instrução:** manter o mesmo papel e orientação; acrescentar uma lista numerada dos passos já cadastrados; identificar fonte, URL, data e aviso; não inventar etapas, solicitar dados pessoais ou alegar atendimento oficial.

**Formato:** identificador/título → orientação → passos numerados → fonte → data → aviso → identificação de protótipo não oficial.

Os passos são revisados junto da orientação e da fonte. O programa apenas os apresenta; não os deduz automaticamente do texto.

## Comparação controlada

O mesmo gabarito de 26 casos foi aplicado a A e B, totalizando 52 execuções. A busca é idêntica; varia apenas a formatação quando existe orientação localizada. A mesma recusa ou solicitação de esclarecimento é usada nos dois modelos quando não há resposta única.

| Critério | A | B |
|---|---|---|
| Orientação preservada | Parágrafo cadastrado | Mesmo parágrafo cadastrado |
| Fonte, data e aviso | Explícitos | Explícitos |
| Sequência de ação | Embutida no texto | Também destacada em itens numerados |
| Extensão | Menor | Maior, porque inclui os passos |
| Resultado na amostra | 26/26 comportamentos corretos | 26/26 comportamentos corretos |

O arquivo `resultados/comparacao_modelos.csv` registra por caso e modelo a presença da fonte, data e aviso, a preservação da orientação, ausência de URL adicional e estrutura esperada. `resultados/testes.csv` contém as respostas completas para comparação. Nas 18 perguntas com orientação localizada em cada modelo, as verificações objetivas passaram; nas recusas/ambiguidades/vazia, a formatação da orientação não se aplica.

**Escolha:** B é o padrão porque explicita a sequência de consulta em itens numerados e mantém fonte e limites visíveis. A é uma alternativa mais curta para leitura rápida. A consistência de conteúdo foi equivalente nesta amostra; nenhuma nota humana de clareza foi atribuída. A vantagem de clareza de B é uma justificativa de estrutura, que ainda precisa ser validada com pessoas do público beneficiado.

Para reproduzir a comparação visual da mesma pergunta:

```bash
python src/sistema.py --pergunta "Como acessar a CNH digital?" --modelo A
python src/sistema.py --pergunta "Como acessar a CNH digital?" --modelo B
```

O roteiro U06 também troca os modelos pelo menu e executa a consulta nos dois formatos. Ambos exibem o canal oficial, a data de verificação e o limite de que a orientação se refere ao acesso digital da habilitação existente.
