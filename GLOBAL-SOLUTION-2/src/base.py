"""Leitura, validação e índices de uma base pequena em JSON."""

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


TEMAS = {
    "conta_govbr": "Conta gov.br",
    "documentos": "Documentos digitais",
    "servicos_cidadao": "Serviços ao cidadão",
}

# Grafo não direcionado: a conta permite acessar documentos e serviços;
# documentos podem ser necessários nos serviços. Os três temas se conectam.
GRAFO_TEMAS = {
    "conta_govbr": ["documentos", "servicos_cidadao"],
    "documentos": ["conta_govbr", "servicos_cidadao"],
    "servicos_cidadao": ["conta_govbr", "documentos"],
}


class BaseInvalida(ValueError):
    """Erro compreensível de arquivo ou conteúdo da base."""


def _texto(valor):
    return isinstance(valor, str) and bool(valor.strip())


def _lista_textos(valor, permitir_vazia=False):
    return (
        isinstance(valor, list)
        and (permitir_vazia or bool(valor))
        and all(_texto(item) for item in valor)
    )


def _fonte_oficial(fonte):
    if not isinstance(fonte, dict) or not _texto(fonte.get("titulo")):
        return False
    url = fonte.get("url")
    if not _texto(url) or any(caractere.isspace() for caractere in url):
        return False
    try:
        endereco = urlparse(url)
        dominio = endereco.hostname or ""
        oficial = any(
            dominio == final or dominio.endswith("." + final)
            for final in ("gov.br", "jus.br", "leg.br")
        )
        return (
            endereco.scheme == "https"
            and oficial
            and endereco.username is None
            and endereco.password is None
            and endereco.port in (None, 443)
        )
    except ValueError:
        return False


def carregar_base(caminho):
    """Carrega todos os registros ou informa por que o arquivo é inválido.

    O mínimo de 15 registros é uma exigência da entrega, conferida na avaliação.
    O carregador também aceita bases menores para manutenção e testes.
    """
    try:
        conteudo = Path(caminho).read_text(encoding="utf-8-sig")
    except FileNotFoundError as erro:
        raise BaseInvalida("Arquivo da base não encontrado. Confira dados/base_conhecimento.json.") from erro
    except (OSError, UnicodeError) as erro:
        raise BaseInvalida("Não foi possível ler a base em UTF-8. Confira o arquivo e a permissão de leitura.") from erro
    if not conteudo.strip():
        raise BaseInvalida("O arquivo da base está vazio. Acrescente orientações antes de consultar.")
    try:
        registros = json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise BaseInvalida(f"JSON inválido na base, linha {erro.lineno}. Confira vírgulas e aspas.") from erro
    if not isinstance(registros, list) or not registros:
        raise BaseInvalida("A base deve ser uma lista JSON com pelo menos uma orientação.")

    identificadores = set()
    campos_texto = ("id", "tema", "titulo", "pergunta", "orientacao", "verificado_em", "aviso")
    for numero, registro in enumerate(registros, 1):
        if not isinstance(registro, dict):
            raise BaseInvalida(f"O registro {numero} deve ser um objeto JSON.")
        for campo in campos_texto:
            if not _texto(registro.get(campo)):
                raise BaseInvalida(f"Registro {numero}: o campo '{campo}' precisa de texto não vazio.")
        identificador = registro["id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", identificador):
            raise BaseInvalida(f"Identificador inválido no registro {numero}. Use letras, números, _ ou -.")
        if identificador in identificadores:
            raise BaseInvalida(f"Identificador repetido: {identificador}.")
        identificadores.add(identificador)
        if registro["tema"] not in TEMAS:
            raise BaseInvalida(f"{identificador}: tema desconhecido. Use um dos três temas disponíveis.")
        for campo in ("palavras_chave", "passos"):
            if not _lista_textos(registro.get(campo)):
                raise BaseInvalida(f"{identificador}: '{campo}' deve ser uma lista de textos não vazios.")
        relacionados = registro.get("relacionados")
        if not _lista_textos(relacionados, permitir_vazia=True):
            raise BaseInvalida(f"{identificador}: 'relacionados' deve ser uma lista de identificadores.")
        if len(relacionados) != len(set(relacionados)) or identificador in relacionados:
            raise BaseInvalida(f"{identificador}: relações repetidas ou com o próprio registro.")
        if not _fonte_oficial(registro.get("fonte")):
            raise BaseInvalida(f"{identificador}: informe título e fonte HTTPS oficial gov.br, jus.br ou leg.br.")
        try:
            data_verificacao = date.fromisoformat(registro["verificado_em"])
            if data_verificacao.isoformat() != registro["verificado_em"]:
                raise ValueError
        except ValueError as erro:
            raise BaseInvalida(f"{identificador}: data de verificação inválida. Use AAAA-MM-DD.") from erro

    for registro in registros:
        if any(item not in identificadores for item in registro["relacionados"]):
            raise BaseInvalida(f"{registro['id']}: há um assunto relacionado inexistente na base.")
    return registros


def criar_indices(registros):
    """Usa dicionários para recuperar por ID e agrupar listas por tema."""
    por_id = {registro["id"]: registro for registro in registros}
    por_tema = {tema: [] for tema in TEMAS}
    for registro in registros:
        por_tema[registro["tema"]].append(registro)
    return {"por_id": por_id, "por_tema": por_tema}
