# 💻 CompuBot — Assistente Virtual de Informática

> Chatbot de atendimento desenvolvido para a disciplina de **Inteligência Artificial**.  
> Responde perguntas sobre informática e computação via interface web (sala de bate-papo).

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Como Rodar os Testes](#como-rodar-os-testes)
- [Perguntas Suportadas](#perguntas-suportadas)
- [Arquitetura do Sistema](#arquitetura-do-sistema)

---

## Sobre o Projeto

O **CompuBot** é um robô de atendimento (chatterbot) especializado no tema de **informática e computação**. O tema foi escolhido em continuidade ao projeto anterior da disciplina — um assistente virtual por voz que executava comandos no sistema operacional usando Whisper e NLTK.

O chatbot é capaz de responder perguntas sobre:

- Sistemas operacionais
- Navegadores e como acessá-los
- Editores de código (como o VS Code)
- Controle de volume do sistema
- Como bloquear a tela do computador
- Assistentes virtuais e como funcionam
- Inteligência Artificial
- Reconhecimento de voz e transcrição de áudio
- Atalhos de teclado

Todas as perguntas, variações e respostas são configuradas externamente em um arquivo **JSON**, sem nenhum hardcode no código-fonte. O robô é acessado como um serviço via navegador web.

---

## Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Chatbot / NLP | Python 3.8 + ChatterBot 1.0.4 |
| Servidor web | Flask 2.2.5 |
| Banco de dados | SQLite (via SQLAlchemy) |
| Configuração | JSON externo (`config.json`) |
| Interface web | HTML5 + CSS3 + JavaScript (Fetch API) |
| Testes | Python `unittest` |

---

## Estrutura de Arquivos

```
chatbot-computador/
│
├── app.py              ← Backend: servidor Flask + ChatterBot
├── config.json         ← Dicionário externo com perguntas, variações e respostas
├── test_chatbot.py     ← Testes automatizados (unittest)
│
├── index.html          ← Interface da sala de bate-papo
├── style.css           ← Estilos da interface (tema dark tech)
├── chat.js             ← Lógica JavaScript (comunicação com o backend)
│
└── requirements.txt    ← Dependências Python
```

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8** (recomendado — o ChatterBot 1.0.4 tem incompatibilidades com Python 3.9+)
- **pip** (gerenciador de pacotes Python)
- Um navegador web moderno (Chrome, Firefox, etc.)

Para verificar sua versão do Python:

```bash
python --version
# ou
python3 --version
```

---

## Instalação

### 1. Clone ou extraia o projeto

Se tiver o arquivo ZIP:

```bash
unzip chatbot-computador.zip
cd chatbot-computador
```

### 2. (Recomendado) Crie um ambiente virtual

Usar um ambiente virtual evita conflitos com outras bibliotecas do seu sistema.

```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa no Linux / macOS
source venv/bin/activate

# Ativa no Windows
venv\Scripts\activate
```

Você saberá que está ativo quando o terminal mostrar `(venv)` no início da linha.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> ⚠️ **Se aparecer erro de `time.clock()`** (Python 3.9+):  
> Localize o arquivo `utils.py` do ChatterBot dentro do seu ambiente virtual e substitua `time.clock()` por `time.perf_counter()`. O caminho costuma ser `venv/lib/pythonX.X/site-packages/chatterbot/utils.py`.

---

## Como Executar

### 1. Inicie o servidor backend

No terminal, dentro da pasta do projeto (com o ambiente virtual ativado):

```bash
python app.py
```

Você verá a saída:

```
🔧 Inicializando e treinando o CompuBot...
✅ CompuBot pronto para atendimento em http://localhost:5000
 * Running on http://127.0.0.1:5000
```

> O bot é treinado automaticamente a partir do `config.json` toda vez que o servidor é iniciado.

### 2. Acesse a interface web

Abra o navegador e acesse:

```
http://localhost:5000
```

A sala de bate-papo será exibida e o CompuBot estará pronto para responder.

### 3. Encerrando o servidor

Pressione `Ctrl + C` no terminal para encerrar.

---

## Como Rodar os Testes

Os testes automatizados validam todas as perguntas, saudações e despedidas configuradas no `config.json`.

### Executar todos os testes

```bash
python test_chatbot.py
```

### Executar com saída detalhada (recomendado)

```bash
python -m pytest test_chatbot.py -v
```

ou, sem o pytest:

```bash
python -m unittest test_chatbot.py -v
```

### O que é testado

| Grupo | Quantidade de testes |
|---|---|
| Saudações | 5 variações |
| Despedidas | 3 variações |
| Sistema operacional | 3 variações |
| Abrir navegador | 3 variações |
| Editor de código | 3 variações |
| Ajustar volume | 3 variações |
| Bloquear tela | 3 variações |
| Assistente virtual | 3 variações |
| Inteligência Artificial | 3 variações |
| Reconhecimento de voz | 3 variações |
| Atalhos de teclado | 3 variações |
| Validação do JSON | 5 testes estruturais |
| **Total** | **41 testes** |

Saída esperada ao final:

```
Ran 41 tests in X.XXXs

OK
```

---

## Perguntas Suportadas

O bot responde (no mínimo) às seguintes perguntas, cada uma com 4 variações:

| # | Tema | Exemplo de pergunta |
|---|---|---|
| 1 | Sistema operacional | "O que é um sistema operacional?" |
| 2 | Abrir navegador | "Como abrir o navegador?" |
| 3 | Editor de código | "O que é o VS Code?" |
| 4 | Ajustar volume | "Como aumentar o volume do PC?" |
| 5 | Bloquear tela | "Como bloquear a tela do computador?" |
| 6 | Assistente virtual | "O que é um assistente virtual?" |
| 7 | Inteligência Artificial | "O que é IA?" |
| 8 | Reconhecimento de voz | "Como funciona o reconhecimento de voz?" |
| 9 | Atalhos de teclado | "Quais os principais atalhos do computador?" |

Além disso, o bot reconhece saudações ("olá", "bom dia", "boa tarde"…) e despedidas ("tchau", "obrigado", "até mais"…).

---

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────┐
│                   USUÁRIO (Navegador)                │
│                       index.html                     │
│                 style.css  |  chat.js                │
└──────────────────────┬──────────────────────────────┘
                       │  POST /chat  { mensagem: "..." }
                       │  (Fetch API — JavaScript)
                       ▼
┌─────────────────────────────────────────────────────┐
│              BACKEND — Flask (app.py)               │
│                                                     │
│  Rota GET  /       → Serve index.html               │
│  Rota POST /chat   → Processa mensagem              │
│  Rota GET  /info   → Metadados do bot               │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           CHATTERBOT (NLP — BestMatch)              │
│                                                     │
│  Treinamento ← config.json (dicionário externo)     │
│  Armazenamento → database.sqlite3                   │
└─────────────────────────────────────────────────────┘
```

**Fluxo de uma mensagem:**

1. O usuário digita uma pergunta na interface web
2. O `chat.js` envia a mensagem via `POST` para `/chat` no Flask
3. O Flask repassa ao ChatterBot, que usa o algoritmo `BestMatch` para encontrar a resposta mais similar às frases treinadas
4. A resposta é retornada em JSON e exibida na tela

---

*Disciplina: Inteligência Artificial — Chatbot de Atendimento*
