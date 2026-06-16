"""
config_adapter.py — CompuBot
Adaptador de lógica customizado para o ChatterBot.

Substitui o BestMatch por um matching controlado diretamente
pelo dicionário externo config.json, garantindo que todas as
variações configuradas retornem sempre a resposta correta.
"""

import json
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class ConfigAdapter(LogicAdapter):
    """
    Adaptador que lê o config.json e responde usando:
    1. Match exato (normalizado): confiança 1.0
    2. Similaridade Jaccard entre palavras: melhor score acima de 0.2
    3. Resposta padrão: se nenhum match for suficiente
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        config_path = kwargs.get('config_path', 'config.json')

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Dicionário: variação normalizada → resposta
        self.pares = {}

        for variacao in config['saudacoes']['variacoes']:
            self.pares[variacao.lower().strip()] = config['saudacoes']['resposta']

        for variacao in config['despedidas']['variacoes']:
            self.pares[variacao.lower().strip()] = config['despedidas']['resposta']

        for pergunta in config['perguntas']:
            for variacao in pergunta['variacoes']:
                self.pares[variacao.lower().strip()] = pergunta['resposta']

        self.resposta_padrao = (
            "Desculpe, não entendi sua pergunta. "
            "Tente perguntar sobre sistemas operacionais, editores de código, "
            "atalhos de teclado, assistentes virtuais ou reconhecimento de voz!"
        )

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters=None):
        texto = input_statement.text.lower().strip()

        # ── 1. Match exato ──────────────────────────────────
        if texto in self.pares:
            resposta = Statement(self.pares[texto])
            resposta.confidence = 1.0
            return resposta

        # ── 2. Similaridade Jaccard ──────────────────────────
        tokens_entrada = set(texto.split())
        melhor_score = 0.0
        melhor_resposta = self.resposta_padrao

        for variacao, resposta in self.pares.items():
            tokens_var = set(variacao.split())
            uniao = tokens_entrada | tokens_var
            if uniao:
                score = len(tokens_entrada & tokens_var) / len(uniao)
                if score > melhor_score:
                    melhor_score = score
                    melhor_resposta = resposta

        texto_final = melhor_resposta if melhor_score >= 0.2 else self.resposta_padrao
        resposta = Statement(texto_final)
        resposta.confidence = melhor_score
        return resposta
