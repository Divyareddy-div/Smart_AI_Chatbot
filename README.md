# Smart AI Chatbot 🤖

A complete, multi-interface, rule-based AI Chatbot project developed in Python for a **B.Tech AI Minor Project**. This chatbot implements core Natural Language Processing (NLP) concepts—such as regular expression pattern matching, keyword extraction, state tracking, and intent classification—using purely **Python standard libraries**.

It features **three distinct user interfaces**:
1. 🖥️ **Command Line Interface (CLI)**: Fast, lightweight interactive terminal app (`chatbot.py`).
2. 🎨 **Desktop GUI Application**: Dark-themed graphical desktop app built with `tkinter` (`gui_chatbot.py`).
3. 🌐 **Web Application Interface**: Modern glassmorphic browser app served via built-in `http.server` (`web_chatbot.py` + `index.html`).

---

## 📌 Project Objective

The objective of this project is to build an interactive conversational agent that demonstrates fundamental concepts of Artificial Intelligence and Natural Language Processing without relying on third-party libraries, heavy machine learning packages, or external cloud APIs.

---

## ✨ Features

- 👤 **Session State & Name Memory**: Welcomes the user, asks for their name, and personalizes responses throughout the interaction session.
- 👋 **Greeting & Courtesy Handling**: Understands and responds appropriately to greetings ("Hi", "Hello", "Hey"), pleasantries ("How are you?"), and expressions of gratitude ("Thank you").
- 🧠 **AI Knowledge Base**: Answers fundamental questions about Artificial Intelligence, Machine Learning, Deep Learning, and Natural Language Processing (NLP).
- 🐍 **Python Knowledge Base**: Explains Python features, its creator (Guido van Rossum), data types, and why Python is popular in AI.
- 📅 **Date & Time Display**: Delivers current local date and time on demand using Python's `datetime` module.
- 🔢 **Safe Arithmetic Evaluator**: Parses and computes basic mathematical operations (`+`, `-`, `*`, `/`, `%`, `^`) safely without using unsafe `eval()` calls.
- 😄 **Jokes & AI Facts**: Features a built-in collection of random programming jokes and interesting AI trivia facts.
- 📜 **Interactive Help Menu**: Displays a structured menu of available topics and sample queries when the user types `help`.
- 🤝 **Polite Fallback System**: Handles unrecognized or out-of-domain questions politely with helpful guidance.
- 🚪 **Clean Session Exit**: Terminates gracefully when the user types `bye` or `exit`.

---

## 🛠️ Technologies Used

| Category | Technology |
|---|---|
| **Programming Language** | Python 3.8+ |
| **Interfaces Available** | CLI (`chatbot.py`), Desktop GUI (`gui_chatbot.py`), Web (`web_chatbot.py`) |
| **GUI Framework** | Python Standard `tkinter` |
| **Web Server Framework**| Python Standard `http.server` & REST API endpoint |
| **Standard Libraries** | `datetime`, `random`, `re`, `sys`, `math`, `tkinter`, `http.server`, `json` |
| **External Dependencies** | None (100% Python Standard Library) |

---

## 💡 AI Concepts Implemented

1. **Rule-Based Conversational Engine**: Employs deterministic rule tables mapping input pattern categories to specific answer generator routines.
2. **Intent Classification**: Evaluates input strings using regular expression priority matching to categorize user intent.
3. **Keyword & Entity Extraction**: Identifies key domain terms (e.g., "Python", "Machine Learning", "date", "joke", numbers) within raw natural text.
4. **Stateful Conversation Management**: Maintains session variables (`user_name`, `conversation_count`) across multi-turn interactions.
5. **Robust Input Normalization**: Strips, converts text to lowercase, and handles trailing punctuation to ensure fault-tolerant matching.

---

## 📁 Project Directory Structure

```
Smart_AI_Chatbot/
│
├── chatbot.py                 # Main Python CLI chatbot application
├── gui_chatbot.py             # Desktop Tkinter GUI application
├── web_chatbot.py             # Web application server (HTTP REST API)
├── index.html                 # Modern glassmorphic Web interface
├── test_chatbot.py            # Automated unit test suite (19 test cases)
├── README.md                  # Project overview and user guide
├── requirements.txt           # Dependency declaration (Standard library only)
│
├── screenshots/               # Terminal & interface execution logs
│   └── sample_run.txt
│
└── documentation/             # Comprehensive academic documentation
    └── Project_Report.md      # Detailed B.Tech Minor Project Report
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Option 1: Run Command Line Interface (CLI)
```bash
python chatbot.py
```

### Option 2: Run Desktop GUI Application
```bash
python gui_chatbot.py
```

### Option 3: Run Web Application Server
```bash
python web_chatbot.py
```
*This will start the local HTTP server at `http://localhost:8000` and automatically open your web browser.*

### Option 4: Run Automated Unit Tests
```bash
python -m unittest test_chatbot.py
```

---

## 💬 Sample User Queries

| Category | Example Command / Question |
|---|---|
| **Greetings** | `Hello`, `Hi there`, `Good morning` |
| **Courtesy** | `How are you?`, `Thank you` |
| **AI Q&A** | `What is AI?`, `What is Machine Learning?`, `What is NLP?` |
| **Python Q&A** | `What is Python?`, `Who created Python?`, `What are Python data types?` |
| **Utilities** | `What is today's date?`, `What time is it?` |
| **Math** | `Calculate 15 * 4`, `What is 100 / 5?`, `50 + 25` |
| **Fun** | `Tell me a joke`, `Share an AI fact` |
| **Help & Exit** | `help`, `bye`, `exit` |

---

## 🔮 Future Enhancements

- 🎙️ **Voice Integration**: Adding Speech-to-Text (STT) and Text-to-Speech (TTS) using Python `speech_recognition` and `pyttsx3`.
- 🧠 **Machine Learning Chatbot**: Extending intent matching with TF-IDF vectorization and Naive Bayes / Intent Classification models.
- 💾 **Database Persistence**: Integrating SQLite to store conversation history and user preferences across sessions.
- 🌐 **Cloud Deployment**: Packaging the Web Application with Docker or Flask/FastAPI for cloud deployment.

---

## 📄 License
This project is open-source and intended for academic and educational purposes under the B.Tech Artificial Intelligence curriculum.
