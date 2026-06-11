"""
test_chatbot.py — CompuBot
Testes automatizados com unittest.

Como executar:
    python -m pytest test_chatbot.py -v
    ou
    python test_chatbot.py
"""

import os
import json
import logging
import unittest

logging.disable(logging.CRITICAL)

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
TEST_DB = os.path.join(BASE_DIR, 'test_database.sqlite3')


class TestCompuBot(unittest.TestCase):
    """Suite de testes para o CompuBot."""

    # ─────────────────────────────────────────────
    # Configuração da suite (executa uma vez)
    # ─────────────────────────────────────────────

    @classmethod
    def setUpClass(cls):
        """Instancia e treina o bot antes de todos os testes."""
        # Garante banco de teste limpo
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            cls.config = json.load(f)

        cls.bot = ChatBot(
            'CompuBotTest',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{TEST_DB}',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Não entendi.',
                    'maximum_similarity_threshold': 0.65
                }
            ],
            read_only=False
        )

        trainer = ListTrainer(cls.bot)

        for variacao in cls.config['saudacoes']['variacoes']:
            trainer.train([variacao, cls.config['saudacoes']['resposta']])

        for variacao in cls.config['despedidas']['variacoes']:
            trainer.train([variacao, cls.config['despedidas']['resposta']])

        for pergunta in cls.config['perguntas']:
            for variacao in pergunta['variacoes']:
                trainer.train([variacao, pergunta['resposta']])

    @classmethod
    def tearDownClass(cls):
        """Remove o banco de dados de teste após todos os testes."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    # ─────────────────────────────────────────────
    # Métodos auxiliares
    # ─────────────────────────────────────────────

    def _tema(self, tema):
        """Retorna a pergunta do config.json pelo tema."""
        for p in self.config['perguntas']:
            if p['tema'] == tema:
                return p
        self.fail(f"Tema '{tema}' não encontrado no config.json")

    def _verificar(self, entrada, esperado):
        """Envia uma mensagem ao bot e compara com o esperado."""
        resposta = str(self.bot.get_response(entrada))
        self.assertEqual(
            resposta, esperado,
            f"\n[ENTRADA]  {entrada}"
            f"\n[ESPERADO] {esperado}"
            f"\n[OBTIDO]   {resposta}"
        )

    # ─────────────────────────────────────────────
    # Testes de Saudações
    # ─────────────────────────────────────────────

    def test_saudacao_ola(self):
        self._verificar('olá', self.config['saudacoes']['resposta'])

    def test_saudacao_oi(self):
        self._verificar('oi', self.config['saudacoes']['resposta'])

    def test_saudacao_bom_dia(self):
        self._verificar('bom dia', self.config['saudacoes']['resposta'])

    def test_saudacao_boa_tarde(self):
        self._verificar('boa tarde', self.config['saudacoes']['resposta'])

    def test_saudacao_boa_noite(self):
        self._verificar('boa noite', self.config['saudacoes']['resposta'])

    # ─────────────────────────────────────────────
    # Testes de Despedidas
    # ─────────────────────────────────────────────

    def test_despedida_tchau(self):
        self._verificar('tchau', self.config['despedidas']['resposta'])

    def test_despedida_ate_mais(self):
        self._verificar('até mais', self.config['despedidas']['resposta'])

    def test_despedida_obrigado(self):
        self._verificar('obrigado', self.config['despedidas']['resposta'])

    # ─────────────────────────────────────────────
    # Sistema Operacional
    # ─────────────────────────────────────────────

    def test_sistema_operacional_variacao_1(self):
        p = self._tema('o_que_e_sistema_operacional')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_sistema_operacional_variacao_2(self):
        p = self._tema('o_que_e_sistema_operacional')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_sistema_operacional_variacao_3(self):
        p = self._tema('o_que_e_sistema_operacional')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Abrir Navegador
    # ─────────────────────────────────────────────

    def test_navegador_variacao_1(self):
        p = self._tema('como_abrir_navegador')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_navegador_variacao_2(self):
        p = self._tema('como_abrir_navegador')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_navegador_variacao_3(self):
        p = self._tema('como_abrir_navegador')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Editor de Código
    # ─────────────────────────────────────────────

    def test_editor_codigo_variacao_1(self):
        p = self._tema('o_que_e_editor_de_codigo')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_editor_codigo_variacao_2(self):
        p = self._tema('o_que_e_editor_de_codigo')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_editor_codigo_variacao_3(self):
        p = self._tema('o_que_e_editor_de_codigo')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Ajustar Volume
    # ─────────────────────────────────────────────

    def test_volume_variacao_1(self):
        p = self._tema('como_ajustar_volume')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_volume_variacao_2(self):
        p = self._tema('como_ajustar_volume')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_volume_variacao_3(self):
        p = self._tema('como_ajustar_volume')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Bloquear Tela
    # ─────────────────────────────────────────────

    def test_bloquear_tela_variacao_1(self):
        p = self._tema('como_bloquear_tela')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_bloquear_tela_variacao_2(self):
        p = self._tema('como_bloquear_tela')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_bloquear_tela_variacao_3(self):
        p = self._tema('como_bloquear_tela')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Assistente Virtual
    # ─────────────────────────────────────────────

    def test_assistente_virtual_variacao_1(self):
        p = self._tema('o_que_e_assistente_virtual')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_assistente_virtual_variacao_2(self):
        p = self._tema('o_que_e_assistente_virtual')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_assistente_virtual_variacao_3(self):
        p = self._tema('o_que_e_assistente_virtual')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Inteligência Artificial
    # ─────────────────────────────────────────────

    def test_inteligencia_artificial_variacao_1(self):
        p = self._tema('o_que_e_inteligencia_artificial')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_inteligencia_artificial_variacao_2(self):
        p = self._tema('o_que_e_inteligencia_artificial')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_inteligencia_artificial_variacao_3(self):
        p = self._tema('o_que_e_inteligencia_artificial')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Reconhecimento de Voz
    # ─────────────────────────────────────────────

    def test_reconhecimento_voz_variacao_1(self):
        p = self._tema('o_que_e_reconhecimento_de_voz')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_reconhecimento_voz_variacao_2(self):
        p = self._tema('o_que_e_reconhecimento_de_voz')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_reconhecimento_voz_variacao_3(self):
        p = self._tema('o_que_e_reconhecimento_de_voz')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Atalhos de Teclado
    # ─────────────────────────────────────────────

    def test_atalhos_teclado_variacao_1(self):
        p = self._tema('atalhos_de_teclado')
        self._verificar(p['variacoes'][0], p['resposta'])

    def test_atalhos_teclado_variacao_2(self):
        p = self._tema('atalhos_de_teclado')
        self._verificar(p['variacoes'][1], p['resposta'])

    def test_atalhos_teclado_variacao_3(self):
        p = self._tema('atalhos_de_teclado')
        self._verificar(p['variacoes'][2], p['resposta'])

    # ─────────────────────────────────────────────
    # Validação da Estrutura do config.json
    # ─────────────────────────────────────────────

    def test_json_possui_campos_obrigatorios(self):
        """config.json deve conter todos os campos obrigatórios."""
        for campo in ('bot_name', 'descricao', 'saudacoes', 'despedidas', 'perguntas'):
            self.assertIn(campo, self.config,
                          f"Campo obrigatório '{campo}' ausente no config.json")

    def test_minimo_sete_perguntas_configuradas(self):
        """O trabalho exige no mínimo 7 perguntas além das saudações."""
        self.assertGreaterEqual(
            len(self.config['perguntas']), 7,
            "O config.json deve ter no mínimo 7 perguntas"
        )

    def test_cada_pergunta_possui_tres_variacoes(self):
        """O trabalho exige pelo menos 3 variações por pergunta."""
        for p in self.config['perguntas']:
            self.assertGreaterEqual(
                len(p['variacoes']), 3,
                f"Tema '{p['tema']}' tem menos de 3 variações"
            )

    def test_cada_pergunta_possui_resposta_nao_vazia(self):
        """Toda pergunta deve ter uma resposta definida e não vazia."""
        for p in self.config['perguntas']:
            self.assertIn('resposta', p,
                          f"Tema '{p['tema']}' não tem campo 'resposta'")
            self.assertTrue(
                len(p['resposta'].strip()) > 0,
                f"Tema '{p['tema']}' tem resposta vazia"
            )

    def test_saudacoes_possuem_variacoes_e_resposta(self):
        """Saudações devem ter variações e uma resposta definida."""
        saudacoes = self.config['saudacoes']
        self.assertIn('variacoes', saudacoes)
        self.assertIn('resposta', saudacoes)
        self.assertGreater(len(saudacoes['variacoes']), 0)

    def test_despedidas_possuem_variacoes_e_resposta(self):
        """Despedidas devem ter variações e uma resposta definida."""
        despedidas = self.config['despedidas']
        self.assertIn('variacoes', despedidas)
        self.assertIn('resposta', despedidas)
        self.assertGreater(len(despedidas['variacoes']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
