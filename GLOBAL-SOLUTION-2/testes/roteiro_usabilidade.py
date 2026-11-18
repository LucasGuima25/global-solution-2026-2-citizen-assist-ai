"""Executa tarefas reais do menu; não representa um teste com participante humano."""

import csv
import json
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter


RAIZ = Path(__file__).resolve().parents[1]
TAREFAS = [
    {
        "id": "U01", "tarefa": "Perguntar e localizar orientação com fonte",
        "entradas": ["1", "Como recuperar a senha da conta gov.br?", "0", "0"],
        "esperado": ["GOV02 -", "Fonte:", "Verificado em:", "Atenção:", "Consulta encerrada."],
    },
    {
        "id": "U02", "tarefa": "Navegar por três assuntos relacionados",
        "entradas": ["2", "1", "1", "1", "1", "0", "0", "0"],
        "esperado": ["GOV01 -", "GOV02 -", "GOV04 -", "Continuar por um assunto relacionado:", "Consulta encerrada."],
    },
    {
        "id": "U03", "tarefa": "Recuperar-se de opção inexistente e entrada vazia",
        "entradas": ["9", "1", "", "0"],
        "esperado": ["Opção inválida.", "Digite uma pergunta", "Temas:", "Consulta encerrada."],
    },
    {
        "id": "U04", "tarefa": "Esclarecer consulta ambígua por seleção",
        "entradas": ["1", "documento digital", "1", "0", "0"],
        "esperado": ["Escolha o assunto que corresponde", "DOC01 -", "Fonte:", "Consulta encerrada."],
    },
    {
        "id": "U05", "tarefa": "Consultar assunto fora da base e encontrar alternativas",
        "entradas": ["1", "Como emitir meu passaporte?", "0"],
        "esperado": ["base", "Temas:", "Documentos digitais", "Consulta encerrada."],
        "proibido": ["DOC02 -", "CID04 -"],
    },
    {
        "id": "U06", "tarefa": "Trocar modelo e repetir a mesma pergunta",
        "entradas": ["3", "A", "1", "Como acessar a CNH digital?", "0", "3", "B", "1", "Como acessar a CNH digital?", "0", "0"],
        "esperado": ["Modelo A selecionado.", "Modelo B selecionado.", "DOC02 -", "Como consultar:", "Consulta encerrada."],
    },
]


def main():
    destino = RAIZ / "resultados"
    transcricoes = destino / "transcricoes"
    transcricoes.mkdir(parents=True, exist_ok=True)
    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
    resultados = []
    for tarefa in TAREFAS:
        inicio = perf_counter()
        processo = subprocess.run(
            [sys.executable, "src/sistema.py"],
            input="\n".join(tarefa["entradas"]) + "\n",
            text=True, encoding="utf-8", capture_output=True,
            cwd=RAIZ, env=ambiente, timeout=15,
        )
        duracao = perf_counter() - inicio
        saida = processo.stdout + processo.stderr
        faltantes = [item for item in tarefa["esperado"] if item not in saida]
        indevidos = [item for item in tarefa.get("proibido", []) if item in saida]
        correto = processo.returncode == 0 and not faltantes and not indevidos
        observacoes = (
            "Percurso concluído. Não houve avaliação com participante humano."
            if correto else f"Código {processo.returncode}; ausências={faltantes}; indevidos={indevidos}"
        )
        registro = {
            "id": tarefa["id"], "tarefa": tarefa["tarefa"],
            "entradas": json.dumps(tarefa["entradas"], ensure_ascii=False),
            "resultado_esperado": " | ".join(tarefa["esperado"]),
            "concluida": correto, "tempo_execucao_s": round(duracao, 6),
            "observacoes": observacoes,
        }
        resultados.append(registro)
        (transcricoes / f"{tarefa['id']}.txt").write_text(saida, encoding="utf-8")
    with (destino / "usabilidade.csv").open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(resultados[0]))
        escritor.writeheader()
        escritor.writerows(resultados)
    concluidas = sum(item["concluida"] for item in resultados)
    print(f"Roteiro executado: {concluidas}/{len(resultados)} tarefas concluídas.")
    print("Tempo inclui abertura e execução do programa; não mede velocidade de leitura humana.")
    return 0 if concluidas == len(resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
