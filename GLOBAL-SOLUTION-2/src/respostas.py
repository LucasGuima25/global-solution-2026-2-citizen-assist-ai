"""Dois modelos de instrução aplicados a dados verificados, sem IA externa."""


MODELOS = {
    "A": (
        "Resposta direta: atue como assistente acadêmico de orientação cidadã. "
        "Apresente o título e a orientação cadastrada em um parágrafo. Identifique "
        "fonte, link, data de verificação e aviso. Não acrescente fatos nem alegue "
        "atendimento oficial."
    ),
    "B": (
        "Resumo e passos: atue como assistente acadêmico de orientação cidadã. "
        "Apresente o título, o resumo e os passos já cadastrados em uma lista "
        "numerada. Identifique fonte, link, data de verificação e aviso. Não "
        "invente etapas, não solicite dados pessoais e não alegue atendimento oficial."
    ),
}


def formatar_resposta(registro, modelo="B"):
    """Formata o registro selecionado; a busca trata recusas e ambiguidades."""
    if modelo not in MODELOS:
        raise ValueError("Modelo de resposta inválido. Escolha A ou B.")
    linhas = [f"{registro['id']} - {registro['titulo']}", "", registro["orientacao"]]
    if modelo == "B":
        linhas.extend(["", "Como consultar:"])
        linhas.extend(f"{numero}. {passo}" for numero, passo in enumerate(registro["passos"], 1))
    linhas.extend([
        "",
        f"Fonte: {registro['fonte']['titulo']}",
        registro["fonte"]["url"],
        f"Verificado em: {registro['verificado_em']}",
        f"Atenção: {registro['aviso']}",
        "Protótipo acadêmico. Este assistente não é um canal oficial de atendimento.",
    ])
    return "\n".join(linhas)
