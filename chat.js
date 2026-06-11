/**
 * chat.js — CompuBot
 * Lógica da sala de bate-papo: envia mensagens ao backend Flask
 * e exibe as respostas do ChatterBot na interface.
 */

const API_URL = 'http://localhost:5000/chat';

// Exibe a hora na mensagem inicial
document.getElementById('hora-inicial').textContent = obterHora();

/** Retorna a hora atual no formato HH:MM */
function obterHora() {
    return new Date().toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

/** Clique em uma sugestão: preenche o input e envia */
function enviarSugestao(botao) {
    document.getElementById('user-input').value = botao.textContent.trim();
    removerSugestoes();
    enviarMensagem();
}

/** Detecta a tecla Enter no input */
function verificarEnter(event) {
    if (event.key === 'Enter') {
        enviarMensagem();
    }
}

/** Remove o painel de sugestões */
function removerSugestoes() {
    const sugestoes = document.getElementById('sugestoes');
    if (sugestoes) sugestoes.remove();
}

/** Função principal: envia mensagem e exibe resposta do bot */
async function enviarMensagem() {
    const input   = document.getElementById('user-input');
    const btnEnviar = document.getElementById('send-btn');
    const mensagem  = input.value.trim();

    if (!mensagem) return;

    removerSugestoes();

    // Exibe mensagem do usuário
    adicionarMensagem(mensagem, 'user');
    input.value = '';

    // Bloqueia UI durante a requisição
    btnEnviar.disabled = true;
    input.disabled     = true;

    const idTyping = mostrarTyping();

    try {
        const resposta = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensagem: mensagem })
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP ${resposta.status}`);
        }

        const dados = await resposta.json();
        removerTyping(idTyping);
        adicionarMensagem(dados.resposta, 'bot');

    } catch (erro) {
        removerTyping(idTyping);
        adicionarMensagem(
            '⚠️ Não foi possível conectar ao servidor. ' +
            'Verifique se o backend está rodando: python app.py',
            'bot'
        );
        console.error('Erro ao chamar a API do CompuBot:', erro);

    } finally {
        btnEnviar.disabled = false;
        input.disabled     = false;
        input.focus();
    }
}

/**
 * Cria e insere um balão de mensagem na tela.
 * @param {string} texto - Conteúdo da mensagem
 * @param {string} tipo  - 'bot' ou 'user'
 */
function adicionarMensagem(texto, tipo) {
    const container = document.getElementById('chat-messages');

    const divMensagem = document.createElement('div');
    divMensagem.classList.add('message', tipo === 'bot' ? 'bot-message' : 'user-message');

    const conteudo = document.createElement('div');
    conteudo.classList.add('message-content');
    conteudo.textContent = texto;

    const hora = document.createElement('div');
    hora.classList.add('message-time');
    hora.textContent = obterHora();

    divMensagem.appendChild(conteudo);
    divMensagem.appendChild(hora);
    container.appendChild(divMensagem);

    // Rolagem automática para a última mensagem
    container.scrollTop = container.scrollHeight;
}

/**
 * Exibe o indicador de "bot está digitando..." (três pontos animados).
 * @returns {string} ID único do elemento, para remoção posterior.
 */
function mostrarTyping() {
    const container = document.getElementById('chat-messages');
    const id = 'typing-' + Date.now();

    const div = document.createElement('div');
    div.classList.add('message', 'bot-message', 'typing-indicator');
    div.id = id;

    const conteudo = document.createElement('div');
    conteudo.classList.add('message-content');
    conteudo.innerHTML =
        '<div class="dot"></div>' +
        '<div class="dot"></div>' +
        '<div class="dot"></div>';

    div.appendChild(conteudo);
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;

    return id;
}

/**
 * Remove o indicador de digitação.
 * @param {string} id - ID retornado por mostrarTyping()
 */
function removerTyping(id) {
    const elem = document.getElementById(id);
    if (elem) elem.remove();
}
