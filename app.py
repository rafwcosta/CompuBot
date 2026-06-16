"""
app.py — CompuBot
Backend Flask + ChatterBot para o chatbot de informática.

Como executar:
    python3 app.py

Acesse em: http://localhost:5000
"""

import os
import json
import logging

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

logging.disable(logging.CRITICAL)

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
DB_PATH = os.path.join(BASE_DIR, 'database.sqlite3')


def carregar_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def criar_e_treinar_bot():
    config = carregar_config()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    bot = ChatBot(
        config['bot_name'],
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri=f'sqlite:///{DB_PATH}',
        logic_adapters=[
            {
                'import_path': 'config_adapter.ConfigAdapter',
                'config_path': CONFIG_PATH
            }
        ],
        read_only=False
    )

    # Treinamento com ListTrainer (requisito da disciplina)
    trainer = ListTrainer(bot)

    for variacao in config['saudacoes']['variacoes']:
        trainer.train([variacao, config['saudacoes']['resposta']])

    for variacao in config['despedidas']['variacoes']:
        trainer.train([variacao, config['despedidas']['resposta']])

    for pergunta in config['perguntas']:
        for variacao in pergunta['variacoes']:
            trainer.train([variacao, pergunta['resposta']])

    return bot


print("🔧 Inicializando e treinando o CompuBot...")
chatbot = criar_e_treinar_bot()
print("✅ CompuBot pronto para atendimento em http://localhost:5000")


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/style.css')
def estilos():
    return send_from_directory(BASE_DIR, 'style.css')

@app.route('/chat.js')
def javascript():
    return send_from_directory(BASE_DIR, 'chat.js')

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()

    if not dados or 'mensagem' not in dados:
        return jsonify({'erro': 'Campo "mensagem" ausente'}), 400

    mensagem = dados['mensagem'].strip()
    if not mensagem:
        return jsonify({'erro': 'Mensagem vazia'}), 400

    resposta = chatbot.get_response(mensagem)
    return jsonify({'resposta': str(resposta)})

@app.route('/info', methods=['GET'])
def info():
    config = carregar_config()
    return jsonify({
        'nome': config['bot_name'],
        'descricao': config['descricao'],
        'total_perguntas': len(config['perguntas'])
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
