"""Avalia os dois modelos no mesmo gabarito; usa apenas a biblioteca padrão."""

import argparse
import csv
import json
import platform
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.base import carregar_base, criar_indices
from src.busca import consultar
from src.respostas import formatar_resposta


def normalizar_texto(texto):
    return " ".join(texto.split())


def verificar_resposta(registro, resposta, modelo):
    """Verificações objetivas de preservação; não substituem revisão humana."""
    fonte = registro["fonte"]["url"]
    passos = registro["passos"]
    return {
        "fonte": fonte in resposta,
        "data": registro["verificado_em"] in resposta,
        "aviso": not registro["aviso"] or registro["aviso"] in resposta,
        "orientacao_preservada": normalizar_texto(registro["orientacao"]) in normalizar_texto(resposta),
        "sem_url_adicional": all(url.rstrip(".,;)") == fonte.rstrip("/") or url.rstrip(".,;)") == fonte
                                  for url in re.findall(r"https?://[^\s<>]+", resposta)),
        "estrutura": modelo == "A" or all(
            f"{numero}. {passo}" in resposta for numero, passo in enumerate(passos, 1)
        ),
    }


def salvar_csv(caminho, linhas):
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
        escritor.writeheader()
        escritor.writerows(linhas)


def executar(base, casos, saida):
    registros = carregar_base(base)
    por_id = criar_indices(registros)["por_id"]
    conjunto = json.loads(casos.read_text(encoding="utf-8"))["casos"]
    if len({caso["id"] for caso in conjunto}) != len(conjunto) or len(conjunto) < 12:
        raise ValueError("O conjunto precisa de pelo menos 12 casos com IDs distintos.")
    resultados, comparacao = [], []
    for modelo in ("A", "B"):
        for caso in conjunto:
            esperado = por_id.get(caso["registro_esperado"])
            if caso["registro_esperado"] and esperado is None:
                raise ValueError(f"Gabarito {caso['id']} aponta registro ausente na base.")
            inicio = perf_counter()
            obtido = consultar(caso["pergunta"], registros)
            registro = obtido["registro"]
            resposta = (formatar_resposta(registro, modelo=modelo)
                        if obtido["status"] == "encontrado" and registro
                        else obtido["mensagem"])
            tempo_ms = (perf_counter() - inicio) * 1000
            acerto = (obtido["status"] == caso["status_esperado"]
                      and (registro["id"] if registro else None) == caso["registro_esperado"])
            checagens = verificar_resposta(registro, resposta, modelo) if registro else {}
            if checagens:
                acerto = acerto and all(checagens.values())
            if obtido["status"] == "ambiguo":
                acerto = acerto and len(obtido["candidatos"]) >= 2
            resultados.append({
                "teste": caso["id"], "categoria": caso["categoria"], "modelo": modelo,
                "pergunta": caso["pergunta"], "status_esperado": caso["status_esperado"],
                "registro_esperado": caso["registro_esperado"] or "",
                "resposta_esperada": esperado["orientacao"] if esperado else caso["status_esperado"],
                "fonte_esperada": esperado["fonte"]["url"] if esperado else "",
                "status_obtido": obtido["status"], "registro_obtido": registro["id"] if registro else "",
                "resposta_obtida": resposta,
                "candidatos": ";".join(item["id"] for item in obtido["candidatos"]),
                "acerto": int(acerto), "tempo_ms": round(tempo_ms, 6),
            })
            comparacao.append({
                "teste": caso["id"], "modelo": modelo, "status": obtido["status"],
                **{chave: int(checagens[chave]) if checagens else "nao_aplicavel"
                   for chave in ("fonte", "data", "aviso", "orientacao_preservada", "sem_url_adicional", "estrutura")},
            })
    indicadores = {
        "executado_em_utc": datetime.now(timezone.utc).isoformat(),
        "casos_distintos": len(conjunto),
        "perguntas_nao_vazias": sum(bool(caso["pergunta"].strip()) for caso in conjunto),
        "categorias": dict(Counter(caso["categoria"] for caso in conjunto)),
        "ambiente": {"python": platform.python_version(), "sistema": platform.platform(),
                     "medicao": "perf_counter; busca e formatação; exclui leitura inicial e digitação"},
        "por_modelo": {},
        "comparacao": "Checagens automáticas de fonte, data, aviso, preservação da orientação e estrutura; sem notas humanas de clareza.",
        "limitacoes": [
            "A amostra é pequena e não representa todas as formulações possíveis.",
            "Checagens textuais não comprovam correção semântica integral nem atualização da fonte.",
            "O tempo depende do equipamento; não mede leitura pelo usuário nem serviços externos.",
            "Facilidade de uso e escolha qualitativa entre modelos exigem roteiro registrado separadamente.",
        ],
    }
    for modelo in ("A", "B"):
        linhas = [linha for linha in resultados if linha["modelo"] == modelo]
        corretos = sum(linha["acerto"] for linha in linhas)
        indicadores["por_modelo"][modelo] = {
            "consultas": len(linhas), "acertos": corretos,
            "taxa_acerto_percentual": round(corretos / len(linhas) * 100, 2),
            "tempo_medio_ms": round(statistics.mean(linha["tempo_ms"] for linha in linhas), 6),
            "falhas": [linha["teste"] for linha in linhas if not linha["acerto"]],
            "por_categoria": {
                categoria: {
                    "casos": sum(linha["categoria"] == categoria for linha in linhas),
                    "acertos": sum(linha["acerto"] for linha in linhas if linha["categoria"] == categoria),
                }
                for categoria in indicadores["categorias"]
            },
        }
    saida.mkdir(parents=True, exist_ok=True)
    salvar_csv(saida / "testes.csv", resultados)
    salvar_csv(saida / "comparacao_modelos.csv", comparacao)
    (saida / "indicadores.json").write_text(json.dumps(indicadores, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for modelo, valores in indicadores["por_modelo"].items():
        print(f"Modelo {modelo}: {valores['acertos']}/{valores['consultas']} corretos "
              f"({valores['taxa_acerto_percentual']}%); média {valores['tempo_medio_ms']:.3f} ms")
        if valores["falhas"]:
            print("  Falhas: " + ", ".join(valores["falhas"]))
    print(f"Evidências gravadas em: {saida}")
    return 0 if all(linha["acerto"] for linha in resultados) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=RAIZ / "dados" / "base_conhecimento.json")
    parser.add_argument("--casos", type=Path, default=Path(__file__).with_name("casos_teste.json"))
    parser.add_argument("--saida", type=Path, default=RAIZ / "resultados")
    args = parser.parse_args()
    return executar(args.base, args.casos, args.saida)


if __name__ == "__main__":
    raise SystemExit(main())
