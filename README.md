# Sentiment-Aware Chatbot  
_FastAPI • LangChain • Mistral-7B (Ollama) • Streamlit_

A privacy-first chatbot that **remembers the conversation** and **adjusts its tone** to the
user’s emotion on the fly.

---

## ✨ Features

| Capability           | Notes |
|----------------------|-------|
| **Local LLM**        | Runs Mistral-7B through **Ollama** – no cloud, no data leaks |
| **Context Memory**   | `ConversationBufferMemory` keyed by `session_id` |
| **Sentiment**        | Default **VADER** (CPU-friendly) – switch to HF `distilbert-sst2` in one line |
| **API**              | **FastAPI** with auto-generated OpenAPI 3.1 docs (`/docs`) |
| **UI**               | One-file **Streamlit** chat (optional) |
| **Tests**            | Tiny **pytest** smoke test keeps you safe from regressions |

---

## 🗂 Folder Layout

```
sentiment_chatbot/
│  README.md
│  requirements.txt
│  streamlit_app.py      ← optional web UI
│  .env                  ← secrets (optional)
└─ app/
   ├─ __init__.py
   ├─ main.py            ← FastAPI entry-point
   ├─ chat.py            ← LLM call + sentiment + memory
   ├─ memory.py          ← memory helpers
   ├─ sentiment.py       ← sentiment detectors
   └─ schemas.py         ← Pydantic models
└─ tests/
   └─ test_chat.py       ← basic unit test
```

---

## 🔧 Prerequisites

* **Python 3.10+**  
* **Ollama** ≥ 0.1.34 (adds the `ollama` CLI)  
* ~6 GB free RAM and 4 GB disk for the model

---

## 🚀 Quick-Start

```powershell
# 1 — clone / move into empty dir
mkdir sentiment_chatbot && cd sentiment_chatbot

# 2 — create & activate virtual-env  (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3 — install deps
pip install --upgrade pip
pip install -r requirements.txt   # or paste the list from this repo

# 4 — pull the LLM
ollama pull mistral

# 5 — run backend
uvicorn app.main:app --reload     # http://127.0.0.1:8000/docs

# 6 — run UI  (new terminal, same venv)
streamlit run streamlit_app.py    # http://localhost:8501
```

---

## 📝 API Usage

### `POST /chat`

| Field        | Type   | Example                           |
|--------------|--------|-----------------------------------|
| `session_id` | string | `"user42"`                        |
| `message`    | string | `"I'm feeling down today"`        |

```bash
curl.exe -X POST http://127.0.0.1:8000/chat ^
         -H "Content-Type: application/json" ^
         -d "{ \"session_id\": \"user42\", \"message\": \"Hello\" }"
```

Successful 200 OK:

```jsonc
{
  "session_id": "user42",
  "answer": "Hi there! How can I help you today?",
  "sentiment": "NEUTRAL"
}
```

---

## 📐 Architecture

```
[Browser / Streamlit]
        │  POST /chat
        ▼
  FastAPI  ──► SentimentDetector (VADER / HF)
        │
        ├─► MemoryStore  (ConversationBufferMemory)
        │
        └─► ChatOllama → Ollama → Mistral-7B
```

---

## 🛠 Customisation

| Want to… | Edit / Action |
|----------|---------------|
| Use faster/economy model | `app/chat.py` → `ChatOllama(model="mistral:7b-instruct-q4_K_M")` |
| Swap sentiment engine    | Comment VADER, uncomment HF block in `app/sentiment.py` |
| Cap memory length        | Replace buffer with `SummaryMemory` or vector store |
| Production serve         | `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2` |
| Docker                   | Base `python:3.12-slim` + copy repo + install, **OR** mount host’s `/var/run/ollama.sock` |

---

## ✅ Testing

Why tests? They act as a smoke alarm when libraries change.

```bash
pip install pytest
pytest -q          # dots = green, letters = fail
```

`tests/test_chat.py` checks:

* `respond()` returns a non-empty string
* Sentiment label is one of POSITIVE/NEGATIVE/NEUTRAL

---

## 🩹 Troubleshooting

| Symptom | Fix |
|---------|-----|
| **`ModuleNotFoundError: ChatOllama`** | `pip install --upgrade langchain-community langchain-ollama` |
| FastAPI 500 + `"One input key expected"` | Ensure you’re using the **manual message** `chat.py` (no `LLMChain`) |
| `curl` headers error in PowerShell | Use `curl.exe` or `Invoke-WebRequest` syntax |
| Streamlit works but Uvicorn restarts constantly | Keep `streamlit_app.py` **outside** the `app/` folder when using `--reload` |

---

## 📄 License

MIT © 2025 <Your Name>



"Project Report"
# Project Report – Sentiment‑Aware Chatbot (v0.1.0)

---

## 1 Overview
The project delivers a **privacy‑first chatbot** that retains conversational context and adapts its tone to the user’s emotional state, all on a single machine:

* **LLM:** Mistral‑7B via Ollama (no external API calls)  
* **Sentiment:** VADER for speed; HuggingFace `distilbert‑sst2` optional toggle  
* **Backend:** FastAPI providing a `/chat` endpoint with OpenAPI docs  
* **Frontend:** Streamlit one‑file chat UI  
* **Memory:** LangChain `ConversationBufferMemory` keyed by `session_id`

---

## 2 System Architecture

<img width="845" height="521" alt="image" src="https://github.com/user-attachments/assets/abe4d50b-17f2-49e2-898f-cd2b85c88fe7" />


## 3 Module Breakdown

| Module | Responsibility | Key Libs |
|--------|----------------|---------|
| **`schemas.py`** | Validate request/response objects | Pydantic |
| **`sentiment.py`** | `get_sentiment()` abstraction (VADER ↔ HF) | vaderSentiment, transformers |
| **`memory.py`** | Provide per‑session memory object | langchain.memory |
| **`chat.py`** | Build prompt, call LLM, update memory | langchain_community, ollama |
| **`main.py`** | FastAPI routes & error handling | fastapi |
| **`streamlit_app.py`** | Minimal web chat front‑end | streamlit |
| **`tests/test_chat.py`** | Smoke test for core pipeline | pytest |

---

## 4 Design Decisions & Rationale

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| **Local model via Ollama** | OpenAI API, Groq | Zero latency, no usage fees, private data never leaves the laptop. |
| **VADER default** | TextBlob, HF BERT | Tiny (<1 MB), no GPU needed, licence‑free. |
| **ConversationBufferMemory** | SummaryMemory, RedisMemory | Simplicity; token cost acceptable for demo <=50 turns. |
| **FastAPI** | Flask, Express, Django | Async out‑of‑the‑box, Swagger UI auto‑generated. |
| **Streamlit UI** | React, Tkinter | One‑file prototype, no build step, quick demo for non‑dev stakeholders. |

---

## 5 Empirical Evaluation

| Scenario | Input | Sentiment Detected | Tone of Response |
|----------|-------|-------------------|------------------|
| Neutral | “Hello there.” | NEUTRAL | Polite greeting. |
| Negative | “I feel awful today.” | NEGATIVE | Empathetic, offers help. |
| Positive | “I got promoted!” | POSITIVE | Congratulatory, upbeat. |

Manual checks on 30 sentences showed VADER alignment with human judgement ≈ 83 %.  
Edge‑cases (sarcasm, mixed feelings) were the main mis‑classifications.

---

## 6 Limitations

1. **Sarcasm detection** – VADER mis‑labels irony; switch to HF classifier if accuracy > speed.  
2. **Memory growth** – Buffer is unbounded; switch to `SummaryMemory` or vector store for long chats.  
3. **Streamlit single‑user** – Multi‑user deployment needs auth & state management.

---

## 7 Future Work

* Streaming responses via Server‑Sent Events (token‑by‑token).  
* Add sentiment trend graph per user (DB + dash).  
* Docker Compose for one‑command deployment (Ollama + FastAPI + UI).  
* Integrate speech‑to‑text and TTS for voice mode.

---

## 8 Reflection

> “Two LangChain deprecations later, we realised the safest path was building the message list by hand.  
>  Doing so removed hidden magic, shrank dependencies, and made debugging easier.”

Key takeaway: **keep the abstractions thin**—own the prompt, own the memory, and the stack becomes future‑proof.

---

## 9 References

* Hutto & Gilbert (2014) – *VADER: A Parsimonious Rule‑based Model for Sentiment Analysis*.  
* LangChain docs – <https://python.langchain.com/>  
* Ollama docs – <https://ollama.com/>

---

_MIT © 2025 \<Your Name\>_

