# المُفسِّر — LLM Explainer App

A small LLM chat app used in the **QAcart DeepEval course**.
Give it any topic and it explains it in professional Jordanian Arabic, rendered as Markdown.

- **Backend:** Python + FastAPI
- **LLM:** any model on [OpenRouter](https://openrouter.ai), called with the `openai` SDK
- **Frontend:** one static Arabic (RTL) page in the QAcart theme

---

## Requirements

- Python **3.10+** — check with `python3 --version`
- An **OpenRouter API key** — create one at https://openrouter.ai/keys

## Run it

### 1. Clone the repo

```bash
git clone https://github.com/Hatamleh/llm-explainer-app.git
cd llm-explainer-app
```

### 2. Create a virtual environment and install dependencies

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Add your API key

Copy the example env file:

```bash
cp .env.example .env
```

Open `.env` and put your key in it:

```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
OPENROUTER_MODEL="google/gemini-3.5-flash"
```

> `.env` is git-ignored — never commit your key.

### 4. Start the app

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** and ask about any topic.

To stop the server press `Ctrl + C`.

---

## Project layout

```
app/
  llm.py       ← explain(topic, history) + SYSTEM_PROMPT — the thing we evaluate
  main.py      ← FastAPI: POST /api/explain, serves the UI
static/
  index.html   ← chat page
  style.css    ← QAcart theme
  app.js       ← sends the topic, renders the Markdown answer
requirements.txt
.env.example
```

## Using it from code (for DeepEval)

The LLM logic lives in `app/llm.py`, separate from the web server, so tests can call it directly:

```python
from app.llm import explain

answer = explain("شو هو الـ API؟")
print(answer)
```

Or call the HTTP API while the server is running:

```bash
curl -X POST http://127.0.0.1:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"topic": "شو هو الـ API؟"}'
```

Response:

```json
{ "answer": "…markdown…", "model": "google/gemini-3.5-flash" }
```

## Changing the model

Set `OPENROUTER_MODEL` in `.env` to any model ID from https://openrouter.ai/models
(for example `openai/gpt-5.4-mini` or `anthropic/claude-haiku-4.5`), then restart the server.

## Troubleshooting

| Problem | Fix |
|---|---|
| `uvicorn: command not found` | Activate the virtual environment first (step 2). |
| Error bubble in the chat / `401` | `OPENROUTER_API_KEY` in `.env` is missing or wrong. |
| `Address already in use` | Another app uses port 8000 — run `uvicorn app.main:app --reload --port 8001`. |
