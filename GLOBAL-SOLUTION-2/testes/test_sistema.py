"""Regressões dos contratos de arquivos, consulta e atualização por dados."""

import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.base import BaseInvalida, carregar_base, criar_indices
from src.busca import consultar
from src.respostas import formatar_resposta
from src.sistema import escolher_opcao


class SistemaTestes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registros = carregar_base(RAIZ / "dados" / "base_conhecimento.json")

    def carregar_temporario(self, conteudo):
        with tempfile.TemporaryDirectory(dir=RAIZ / "testes") as pasta:
            caminho = Path(pasta) / "base.json"
            caminho.write_text(conteudo, encoding="utf-8")
            return carregar_base(caminho)

    def test_arquivo_ausente_vazio_e_invalido(self):
        with tempfile.TemporaryDirectory(dir=RAIZ / "testes") as pasta:
            with self.assertRaises(BaseInvalida):
                carregar_base(Path(pasta) / "ausente.json")
        for conteudo in ("", "{json quebrado", "[]", "{}"):
            with self.subTest(conteudo=conteudo), self.assertRaises(BaseInvalida):
                self.carregar_temporario(conteudo)

    def test_registros_incompletos_duplicados_e_fonte_ausente(self):
        for alteracao in ("campo", "duplicado", "fonte"):
            registros = copy.deepcopy(self.registros)
            if alteracao == "campo":
                del registros[0]["orientacao"]
            elif alteracao == "duplicado":
                registros.append(copy.deepcopy(registros[0]))
            else:
                del registros[0]["fonte"]["url"]
            with self.subTest(alteracao=alteracao), self.assertRaises(BaseInvalida):
                self.carregar_temporario(json.dumps(registros, ensure_ascii=False))

    def test_minimos_e_indices_da_base_entregue(self):
        indices = criar_indices(self.registros)
        self.assertGreaterEqual(len(self.registros), 15)
        self.assertGreaterEqual(len({registro["tema"] for registro in self.registros}), 3)
        self.assertTrue(all(indices["por_tema"].values()))
        self.assertEqual(len(indices["por_id"]), len(self.registros))

    def test_atualizacao_da_base_sem_alterar_codigo(self):
        registros = copy.deepcopy(self.registros)
        novo = copy.deepcopy(registros[0])
        novo.update({"id": "BIB01", "titulo": "Renovação de livro na biblioteca",
                     "pergunta": "Como renovar o empréstimo de livro na biblioteca?",
                     "palavras_chave": ["biblioteca", "renovar livro", "emprestimo de livro"],
                     "orientacao": "Consulte a biblioteca para conhecer as regras de renovação.",
                     "passos": ["Consulte a biblioteca para conhecer as regras de renovação."],
                     "relacionados": [registros[0]["id"]]})
        registros.append(novo)
        atualizados = self.carregar_temporario(json.dumps(registros, ensure_ascii=False))
        resposta = consultar("Como renovar o empréstimo de livro na biblioteca?", atualizados)
        self.assertEqual(resposta["status"], "encontrado")
        self.assertEqual(resposta["registro"]["id"], "BIB01")

    def test_pergunta_vazia_nao_seleciona_orientacao(self):
        resposta = consultar("   ", self.registros)
        self.assertEqual(resposta["status"], "invalido")
        self.assertIsNone(resposta["registro"])

    def test_consulta_ambigua_pede_esclarecimento(self):
        resposta = consultar("documento digital", self.registros)
        self.assertEqual(resposta["status"], "ambiguo")
        self.assertIsNone(resposta["registro"])
        self.assertGreaterEqual(len(resposta["candidatos"]), 2)

    def test_termos_compartilhados_nao_autorizam_resposta_fora_escopo(self):
        for pergunta in ("Como recuperar a senha do meu Wi-Fi?",
                         "Como alterar o telefone da minha conta bancária?",
                         "Como emitir meu passaporte?"):
            with self.subTest(pergunta=pergunta):
                resposta = consultar(pergunta, self.registros)
                self.assertEqual(resposta["status"], "sem_resposta")
                self.assertIsNone(resposta["registro"])

    def test_normalizacao_preserva_assunto(self):
        for pergunta in ("COMO ATIVAR A VERIFICAÇÃO EM DUAS ETAPAS NO GOV.BR?",
                         "como ativar a verificacao em duas etapas no gov.br?"):
            with self.subTest(pergunta=pergunta):
                resposta = consultar(pergunta, self.registros)
                self.assertEqual(resposta["status"], "encontrado")
                self.assertEqual(resposta["registro"]["id"], "GOV04")

    def test_assunto_conhecido_nao_cobre_procedimento_ausente(self):
        for pergunta in ("Como renovar minha CNH?", "Como solicitar meu CPF?",
                         "Como emitir meu passaporte?",
                         "Como acessar a conta gov.br de outra pessoa?"):
            with self.subTest(pergunta=pergunta):
                resposta = consultar(pergunta, self.registros)
                self.assertEqual(resposta["status"], "sem_resposta")
                self.assertIsNone(resposta["registro"])

    def test_modelos_preservam_orientacao_fonte_data_e_aviso(self):
        for registro in self.registros:
            for modelo in ("A", "B"):
                with self.subTest(registro=registro["id"], modelo=modelo):
                    resposta = formatar_resposta(registro, modelo=modelo)
                    for trecho in (registro["orientacao"], registro["fonte"]["url"],
                                   registro["verificado_em"], registro["aviso"]):
                        self.assertIn(trecho, resposta)

    def test_acao_inversa_nao_recebe_orientacao_de_ativacao(self):
        for acao in ("desativar", "remover", "desabilitar"):
            pergunta = f"Como {acao} a verificação em duas etapas?"
            with self.subTest(acao=acao):
                resposta = consultar(pergunta, self.registros)
                self.assertEqual(resposta["status"], "sem_resposta")
                self.assertIsNone(resposta["registro"])

    def test_menu_trata_numero_muito_longo_e_permite_continuar(self):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=["9" * 5000, "1"]), contextlib.redirect_stdout(saida):
            escolha = escolher_opcao("Temas", ["Conta gov.br", "Documentos"])
        self.assertEqual(escolha, 0)
        self.assertIn("Opção inválida.", saida.getvalue())


if __name__ == "__main__":
    unittest.main()
