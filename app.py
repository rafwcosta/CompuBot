"""
app.py — CompuBot
Backend Flask + ChatterBot para o chatbot de informática.

Como executar:
    python app.py

Acesse em: http://localhost:5000
"""

import os
import json
import logging

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Silencia logs internos do ChatterBot
logging.disable(logging.CRITICAL)

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend JavaScript

# Caminhos absolutos para evitar problemas de diretório de trabalho
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
DB_PATH = os.path.join(BASE_DIR, 'database.sqlite3')


# ─────────────────────────────────────────────────────────────
# Funções auxiliares
# ─────────────────────────────────────────────────────────────

def carregar_config():
    """Lê e retorna o dicionário de configuração do JSON externo."""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def criar_e_treinar_bot():
    """
    Instancia o ChatterBot e treina com os dados do config.json.
    O banco de dados é recriado a cada inicialização para garantir
    que o treinamento esteja sempre sincronizado com o JSON.
    """
    config = carregar_config()

    # Remove banco existente para treinamento limpo
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    bot = ChatBot(
        config['bot_name'],
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri=f'sqlite:///{DB_PATH}',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': (
                    'Desculpe, não entendi sua pergunta. '
                    'Tente perguntar sobre sistemas operacionais, editores de código, '
                    'atalhos de teclado, assistentes virtuais ou reconhecimento de voz!'
                ),
                'maximum_similarity_threshold': 0.3
            }
        ],
        read_only=False
    )

    trainer = ListTrainer(bot)

    # Treina saudações
    for variacao in config['saudacoes']['variacoes']:
        trainer.train([variacao, config['saudacoes']['resposta']])

    # Treina despedidas
    for variacao in config['despedidas']['variacoes']:
        trainer.train([variacao, config['despedidas']['resposta']])

    # Treina todas as perguntas do domínio
    for pergunta in config['perguntas']:
        for variacao in pergunta['variacoes']:
            trainer.train([variacao, pergunta['resposta']])

    return bot


# ─────────────────────────────────────────────────────────────
# Inicialização do bot na subida do servidor
# ─────────────────────────────────────────────────────────────

print("🔧 Inicializando e treinando o CompuBot...")
chatbot = criar_e_treinar_bot()
print("✅ CompuBot pronto para atendimento em http://localhost:5000")


# ─────────────────────────────────────────────────────────────
# Rotas Flask
# ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve a interface web da sala de bate-papo."""
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/style.css')
def estilos():
    return send_from_directory(BASE_DIR, 'style.css')


@app.route('/chat.js')
def javascript():
    return send_from_directory(BASE_DIR, 'chat.js')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Recebe a mensagem do usuário (JSON) e retorna a resposta do bot.

    Corpo esperado: { "mensagem": "sua pergunta aqui" }
    Retorno:        { "resposta": "resposta do bot" }
    """
    dados = request.get_json()

    if not dados or 'mensagem' not in dados:
        return jsonify({'erro': 'Campo "mensagem" ausente no corpo da requisição'}), 400

    mensagem_usuario = dados['mensagem'].strip()

    if not mensagem_usuario:
        return jsonify({'erro': 'Mensagem não pode ser vazia'}), 400

    resposta = chatbot.get_response(mensagem_usuario)
    return jsonify({'resposta': str(resposta)})


@app.route('/info', methods=['GET'])
def info():
    """Retorna metadados do bot (útil para depuração)."""
    config = carregar_config()
    return jsonify({
        'nome': config['bot_name'],
        'descricao': config['descricao'],
        'total_perguntas': len(config['perguntas'])
    })


# ─────────────────────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)
