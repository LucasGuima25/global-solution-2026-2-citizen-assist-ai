"""Busca lexical conservadora, explicável e sem serviço externo."""

import re
import unicodedata
from collections import Counter

try:
    from .base import TEMAS
except ImportError:  # Execução direta de python src/sistema.py.
    from base import TEMAS


# Palavras de ligação e pedidos genéricos não identificam uma orientação.
IGNORADAS = set(
    "a ao aos as o os de da das do dos e em na nas no nos um uma uns umas "
    "por para pelo pela pelos pelas com sem que qual quais como onde quando "
    "eu meu minha meus minhas se sim nao voce voces isso esse essa este esta "
    "sobre preciso quero posso consigo tenho consultar "
    "acessar baixar ver encontrar usar fazer saber funciona "
    "pode poderia gostaria ajuda ajudar celular aplicativo app internet online "
    "ou depois antes ja tambem mais perto mim "
    "documento digital servico conta govbr".split()
)
EQUIVALENCIAS = {
    "documentos": "documento", "digitais": "digital", "servicos": "servico",
    "contas": "conta", "niveis": "nivel", "veiculos": "veiculo",
    "senhas": "senha", "dados": "dado", "etapas": "etapa",
    "passos": "passo", "esqueci": "recuperar", "perdi": "recuperar",
    "recuperacao": "recuperar", "criacao": "criar", "reclamacoes": "reclamacao",
    "denuncias": "denuncia", "informacoes": "informacao",
}
FORA_ESCOPO = {"falsificar", "fraudar", "invadir", "hackear", "burlar"}

# Ações diferentes não são equivalentes só por mencionarem o mesmo documento.
ACOES = {
    "acessar": "consultar", "abrir": "consultar", "baixar": "consultar",
    "ver": "consultar", "consultar": "consultar", "visualizar": "consultar",
    "criar": "criar", "cadastrar": "criar",
    "recuperar": "recuperar", "recupero": "recuperar", "esqueci": "recuperar",
    "resetar": "recuperar",
    "alterar": "alterar", "trocar": "alterar", "mudar": "alterar", "atualizar": "alterar",
    "ativar": "ativar", "habilitar": "ativar",
    "desativar": "desativar", "remover": "desativar", "desabilitar": "desativar",
    "emitir": "solicitar", "solicitar": "solicitar", "pedir": "solicitar",
    "obter": "solicitar", "tirar": "solicitar",
    "renovar": "renovar", "cancelar": "cancelar", "excluir": "cancelar",
    "localizar": "localizar", "encontrar": "localizar",
    "registrar": "registrar", "reclamar": "registrar",
}


def normalizar(texto):
    """Remove acentos, troca pontuação por espaços e reduz para minúsculas."""
    texto = unicodedata.normalize("NFKD", texto.casefold())
    texto = "".join(letra for letra in texto if not unicodedata.combining(letra))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\bgov\s+br\b", "govbr", texto)
    return " ".join(texto.split())


def _tokens(texto, ignorar_genericas=True):
    palavras = {EQUIVALENCIAS.get(palavra, palavra) for palavra in normalizar(texto).split()}
    return palavras - IGNORADAS if ignorar_genericas else palavras


def _resultado(status, mensagem, candidatos=None, registro=None):
    return {
        "status": status,
        "registro": registro,
        "candidatos": candidatos or [],
        "mensagem": mensagem,
    }


def _acoes(texto):
    return [ACOES[palavra] for palavra in normalizar(texto).split() if palavra in ACOES]


def _consulta_generica(pergunta):
    palavras = _tokens(pergunta, ignorar_genericas=False)
    ligacoes = set("o os a as um uma de da do das dos como qual quais meu minha quero preciso ver consultar sobre".split())
    assunto = palavras - ligacoes
    if assunto and assunto <= {"conta", "govbr"}:
        return "conta_govbr"
    if assunto and assunto <= {"documento", "digital"}:
        return "documentos"
    if assunto and assunto <= {"servico", "cidadao", "publico"}:
        return "servicos_cidadao"
    return None


def consultar(pergunta, registros, tema=None):
    """Compara conjuntos de palavras e evita responder por semelhança fraca.

    Cada palavra compartilhada soma 1/frequência na base. Palavras do título,
    da pergunta e das palavras-chave recebem um ponto adicional. Soma-se a
    cobertura da pergunta. A resposta única exige cobertura >= 75% e palavra presente em
    no máximo dois registros. A primeira ação reconhecida na pergunta precisa
    estar no título, pergunta ou palavras-chave do assunto. Empates próximos
    e consultas genéricas pedem esclarecimento. Essa medida lexical não é
    uma probabilidade de acerto.
    """
    if not isinstance(pergunta, str) or not pergunta.strip():
        return _resultado("invalido", "Digite uma pergunta ou escolha um tema no menu.")
    if tema is not None and tema not in TEMAS:
        return _resultado("invalido", "Tema inexistente. Escolha uma opção do menu.")
    disponiveis = [r for r in registros if tema is None or r["tema"] == tema]
    if not disponiveis:
        return _resultado("sem_resposta", "Não há orientações disponíveis neste tema.")

    palavras_completas = _tokens(pergunta, ignorar_genericas=False)
    if palavras_completas & FORA_ESCOPO:
        return _resultado("sem_resposta", "Essa solicitação não está coberta pela base de orientações verificadas. Consulte um serviço oficial.")
    generico = _consulta_generica(pergunta)
    if generico is not None:
        opcoes = [r for r in disponiveis if r["tema"] == generico]
        if len(opcoes) > 1:
            return _resultado("ambiguo", "Há mais de um assunto possível. Escolha a orientação desejada.", opcoes)

    palavras_pergunta = _tokens(pergunta)
    if not palavras_pergunta:
        return _resultado("sem_resposta", "Sua pergunta precisa indicar um assunto mais específico. Você também pode escolher um tema.")

    vocabularios = []
    for registro in disponiveis:
        texto_principal = " ".join(registro["palavras_chave"] + [registro["titulo"], registro["pergunta"]])
        principais = _tokens(texto_principal)
        texto_completo = " ".join([texto_principal, registro["orientacao"]] + registro["passos"])
        vocabularios.append((registro, principais, _tokens(texto_completo), _acoes(texto_principal)))
    frequencias = Counter(palavra for _, _, palavras, _ in vocabularios for palavra in palavras)
    acoes_pergunta = _acoes(pergunta)

    resultados = []
    for registro, principais, palavras, acoes_assunto in vocabularios:
        if acoes_pergunta and acoes_pergunta[0] not in acoes_assunto:
            continue
        compartilhadas = palavras & palavras_pergunta
        cobertura = len(compartilhadas) / len(palavras_pergunta)
        if compartilhadas and cobertura >= 0.5:
            peso = sum(1 / frequencias[palavra] for palavra in compartilhadas)
            peso += len(compartilhadas & principais)
            forte = any(frequencias[palavra] <= 2 for palavra in compartilhadas)
            resultados.append((peso + cobertura, cobertura, forte, registro))
    resultados.sort(key=lambda item: (-item[0], item[3]["id"]))
    if not resultados:
        return _resultado("sem_resposta", "Não encontrei uma orientação confiável na base para essa pergunta. Escolha um tema ou consulte a fonte oficial adequada.")

    primeiro = resultados[0]
    if primeiro[1] < 0.75 or not primeiro[2]:
        return _resultado("sem_resposta", "A correspondência é insuficiente para orientar com segurança. Especifique o assunto ou escolha uma opção do menu.")
    proximos = [item[3] for item in resultados if primeiro[0] - item[0] <= 0.25]
    if len(proximos) > 1:
        return _resultado("ambiguo", "Encontrei orientações próximas. Escolha uma delas para evitar uma resposta inadequada.", proximos)
    return _resultado("encontrado", "Orientação localizada na base verificada.", registro=primeiro[3])
