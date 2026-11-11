# 🤖 AI Chatbot using Flask, Groq & CrewAI

An intelligent AI-powered chatbot built using **Python, Flask, Groq API, and CrewAI**. It provides conversational responses while maintaining conversation context through memory management and optimizing token usage.

## 🚀 Features

- **AI-Powered Conversations:** Generates responses using Groq's language models.
- **CrewAI Integration:** Uses AI agents and task execution to process user queries.
- **Conversation Memory:** Maintains conversation history for contextual responses.
- **Automatic Summarization:** Summarizes older messages to preserve important context.
- **Token Optimization:** Optimizes conversation messages to reduce unnecessary token usage.
- **Clear Chat:** Allows users to clear their conversation history.
- **Interactive Web Interface:** Simple and user-friendly chatbot interface.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Groq API | AI language model integration |
| CrewAI | AI agent and task management |
| LiteLLM | Language model connectivity |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interactions |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
AI_Chatbot/
│
├── app.py                 # Flask application
├── chatbot.py             # Chatbot engine and AI integration
├── memory_manager.py      # Conversation memory management
├── token_optimizer.py     # Token optimization
├── config.py              # Application configuration
├── .env                   # API keys and environment variables
├── .gitignore             # Files excluded from Git
│
├── templates/
│   └── index.html         # Chatbot user interface
│
├── static/
│   ├── style.css          # Chatbot styling
│   └── script.js          # Frontend functionality
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_Chatbot.git
cd AI_Chatbot
```

### 2. Create a Virtual Environment

```bash
py -m venv venv
```

Activate the environment in
