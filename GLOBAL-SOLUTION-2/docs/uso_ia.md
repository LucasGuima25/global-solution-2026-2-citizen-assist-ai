# Registro de uso de inteligência artificial

Foi utilizado o assistente Codex para apoiar a leitura do enunciado, o planejamento, a pesquisa em páginas oficiais, a implementação Python, a elaboração dos casos de teste e a documentação. A equipe deverá revisar e compreender esses materiais antes de apresentar e entregar o trabalho.

## Como o apoio foi aplicado

| Atividade | Apoio de IA | Verificação realizada |
|---|---|---|
| Requisitos | Organizar as exigências do PDF em tarefas e evidências | Conferência do texto e das páginas renderizadas; as Tabelas 1 e 2 aparecem sem conteúdo |
| Base de conhecimento | Localizar fontes e redigir resumos | Leitura de páginas oficiais, associação de cada orientação à sua fonte e registro da data em `fontes.md` |
| Código | Elaborar funções e interface textual | Execução local, testes de arquivos/consultas, comparação dos modelos e roteiro com o programa real |
| Testes | Propor perguntas, paráfrases e casos de erro | Gabarito explícito, resultados reais salvos por scripts, registro de dificuldades e limitações |
| Documentação | Organizar explicações e roteiro de apresentação | Conferência com os arquivos e com as saídas da versão executada |

Os testes e as verificações automatizadas não substituem a revisão dos integrantes. Não houve ensaio com usuários humanos: a evidência de facilidade de uso é um roteiro de tarefas executado sobre a interface real, modalidade permitida pelo enunciado. A comparação automática dos modelos mede aspectos objetivos de formato e fidelidade, sem simular opinião humana.

## Limites do protótipo

O protótipo não usa modelo generativo, API paga, treinamento ou conexão a serviços externos durante a consulta. Os modelos A e B são instruções e formatos determinísticos: ambos utilizam exclusivamente os campos da base local. Não há geração de fatos nem acesso a contas ou dados pessoais. A busca também não utiliza IA externa.

O programa não consulta versões atualizadas das páginas automaticamente. Cada referência deve ser reaberta por um responsável antes de atualizar o conteúdo e sua data de verificação. A presença de um link oficial não garante que uma orientação continue atual indefinidamente.

## Validação crítica para a apresentação

Antes da entrega, cada integrante deve conseguir explicar a leitura do JSON, a função de listas/dicionários, as regras de busca e ambiguidade, o grafo de assuntos, a diferença entre A/B e o cálculo dos indicadores. Conferir as fontes, reproduzir os comandos do README e registrar correções efetivamente realizadas. Não declarar que houve validação humana, entrevista ou teste com participante se essa atividade não ocorreu.
