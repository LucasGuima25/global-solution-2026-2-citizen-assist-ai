"""Interface textual do Citizen Assist AI. Execute: python src/sistema.py."""

import argparse
from pathlib import Path

if __package__:
    from .base import BaseInvalida, GRAFO_TEMAS, TEMAS, carregar_base, criar_indices
    from .busca import consultar
    from .respostas import MODELOS, formatar_resposta
else:
    from base import BaseInvalida, GRAFO_TEMAS, TEMAS, carregar_base, criar_indices
    from busca import consultar
    from respostas import MODELOS, formatar_resposta


PASTA_PROJETO = Path(__file__).resolve().parents[1]
BASE_PADRAO = PASTA_PROJETO / "dados" / "base_conhecimento.json"
AVISO = (
    "Assistente educativo de orientação cidadã. Não é um canal oficial.\n"
    "As respostas vêm de uma base local e podem exigir confirmação na fonte.\n"
    "Não informe CPF, senha, documentos ou outros dados pessoais.\n"
    "As perguntas não são gravadas nem enviadas a serviços externos."
)


def escolher_opcao(titulo, opcoes):
    """Mostra opções numeradas. Devolve a posição ou None para voltar."""
    while True:
        print(f"\n{titulo}")
        for numero, texto in enumerate(opcoes, 1):
            print(f"{numero}. {texto}")
        print("0. Voltar")
        entrada = input("Escolha: ").strip()
        if entrada == "0":
            return None
        # Uma opção válida não precisa de mais dígitos que a última opção.
        # Limitar antes de int também evita erro para números muito longos.
        if entrada.isascii() and entrada.isdecimal() and len(entrada) <= len(str(len(opcoes))):
            numero = int(entrada)
            if 1 <= numero <= len(opcoes):
                return numero - 1
        print("Opção inválida. Digite um dos números apresentados.")


def mostrar_temas(registros):
    disponiveis = [tema for tema in TEMAS if any(r["tema"] == tema for r in registros)]
    return disponiveis


def navegar_orientacao(registro, indices, modelo):
    """Usa as arestas entre registros para continuar a consulta sem recursão."""
    atual = registro
    while True:
        print("\n" + formatar_resposta(atual, modelo))
        relacionados = [indices["por_id"][codigo] for codigo in atual["relacionados"]]
        if not relacionados:
            return
        escolha = escolher_opcao(
            "Continuar por um assunto relacionado:",
            [r["titulo"] for r in relacionados],
        )
        if escolha is None:
            return
        atual = relacionados[escolha]


def perguntar(registros, indices, modelo, tema=None):
    pergunta = input("\nQual é sua dúvida? (0 para voltar): ").strip()
    if pergunta == "0":
        return
    resultado = consultar(pergunta, registros, tema)
    if resultado["status"] == "encontrado":
        navegar_orientacao(resultado["registro"], indices, modelo)
    elif resultado["status"] == "ambiguo":
        print("\n" + resultado["mensagem"])
        candidatos = resultado["candidatos"]
        escolha = escolher_opcao(
            "Escolha o assunto que corresponde à sua dúvida:",
            [r["titulo"] for r in candidatos],
        )
        if escolha is not None:
            navegar_orientacao(candidatos[escolha], indices, modelo)
    else:
        print("\n" + resultado["mensagem"])
        print("Você pode explorar os temas disponíveis pelo menu principal.")
        print("Temas: " + ", ".join(TEMAS[t] for t in mostrar_temas(registros)))


def explorar_temas(registros, indices, modelo):
    temas = mostrar_temas(registros)
    escolha = escolher_opcao("Temas disponíveis:", [TEMAS[t] for t in temas])
    if escolha is None:
        return
    tema = temas[escolha]
    while True:
        assuntos = indices["por_tema"][tema]
        print(f"\nTema atual: {TEMAS[tema]}")
        vizinhos = [t for t in GRAFO_TEMAS.get(tema, []) if t in temas]
        if vizinhos:
            print("Temas relacionados: " + ", ".join(TEMAS[t] for t in vizinhos))
        opcoes = [r["titulo"] for r in assuntos]
        opcoes.append("Fazer uma pergunta neste tema")
        opcoes.extend("Explorar " + TEMAS[t] for t in vizinhos)
        escolha = escolher_opcao("Assuntos e caminhos de consulta:", opcoes)
        if escolha is None:
            return
        if escolha < len(assuntos):
            navegar_orientacao(assuntos[escolha], indices, modelo)
        elif escolha == len(assuntos):
            perguntar(registros, indices, modelo, tema)
        else:
            tema = vizinhos[escolha - len(assuntos) - 1]


def apresentar_resultado(resultado, modelo):
    """Saída de uma consulta única, útil para demonstrações reproduzíveis."""
    if resultado["status"] == "encontrado":
        print(formatar_resposta(resultado["registro"], modelo))
    else:
        print(resultado["mensagem"])
        if resultado["candidatos"]:
            print("Assuntos possíveis:")
            for candidato in resultado["candidatos"]:
                print(f"- {candidato['id']}: {candidato['titulo']}")
        print("Use o modo interativo para escolher um assunto ou explorar os temas.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Citizen Assist AI - orientação cidadã local")
    parser.add_argument("--base", type=Path, default=BASE_PADRAO, help="Arquivo JSON da base")
    parser.add_argument("--pergunta", help="Executa uma consulta e encerra")
    parser.add_argument("--tema", choices=list(TEMAS), help="Restringe a consulta a um tema")
    parser.add_argument("--modelo", choices=list(MODELOS), default="B", help="Modelo A ou B")
    argumentos = parser.parse_args(argv)
    try:
        registros = carregar_base(argumentos.base)
    except BaseInvalida as erro:
        print(f"Não foi possível iniciar: {erro}")
        print("Confira o arquivo de dados e tente novamente.")
        return 2
    indices = criar_indices(registros)
    print("\nCITIZEN ASSIST AI\n")
    print(AVISO)
    if argumentos.pergunta is not None:
        resultado = consultar(argumentos.pergunta, registros, argumentos.tema)
        apresentar_resultado(resultado, argumentos.modelo)
        return 2 if resultado["status"] == "invalido" else 0

    modelo = argumentos.modelo
    try:
        while True:
            print(f"\nMenu principal | Modelo de resposta: {modelo}")
            print("1. Fazer uma pergunta")
            print("2. Explorar temas e assuntos")
            print("3. Comparar instruções e trocar modelo de resposta")
            print("4. Ver fontes, privacidade e limites")
            print("0. Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "0":
                print("Consulta encerrada.")
                return 0
            if opcao == "1":
                perguntar(registros, indices, modelo)
            elif opcao == "2":
                explorar_temas(registros, indices, modelo)
            elif opcao == "3":
                for codigo, instrucao in MODELOS.items():
                    print(f"\nModelo {codigo}: {instrucao}")
                novo_modelo = input("Escolha A ou B (0 para voltar): ").strip().upper()
                if novo_modelo in MODELOS:
                    modelo = novo_modelo
                    print(f"Modelo {modelo} selecionado.")
                elif novo_modelo != "0":
                    print("Modelo inválido. Escolha A ou B.")
            elif opcao == "4":
                print("\n" + AVISO)
                print("Cada resposta identifica fonte, endereço e data da verificação.")
                print("Não há conexão a órgãos públicos nem consulta a dados individuais.")
                print("A base cobre somente os assuntos apresentados no menu.")
            else:
                print("Opção inválida. Digite 0, 1, 2, 3 ou 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nConsulta encerrada.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
