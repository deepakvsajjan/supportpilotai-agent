# SupportPilot AI — Customer Support Agent

A portfolio project demonstrating a document-grounded support assistant, REST APIs, Python, FastAPI, SQLite persistence, file ingestion, user feedback, validation, and basic tests.

## Features
- Browser chat UI (HTML/CSS/JavaScript)
- FastAPI endpoints: `/health`, `/chat`, `/history/{session_id}`, `/feedback`, `/documents`
- RAG-style retrieval using TF-IDF and cosine similarity
- Optional OpenAI chat completion integration
- Transparent no-key demo mode: returns retrieved text excerpts and clearly does not pretend they are LLM-generated
- TXT, MD and text-based PDF uploads
- SQLite conversation history and feedback
- Basic pytest suite and safety-oriented system instructions

## Architecture
1. Browser sends a question to `POST /chat`.
2. TF-IDF retrieval finds relevant passages from the knowledge base.
3. If `OPENAI_API_KEY` is configured, the LLM receives the question plus retrieved context.
4. The answer, source names and session ID are returned; messages are stored in SQLite.

**Technical honesty:** This starter uses TF-IDF lexical retrieval, not embedding-based semantic search or a vector database. Uploaded documents are indexed in memory and that index resets on server restart.

## Run on Windows PowerShell
Install Python 3.10+ first, then open a terminal in this folder:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal only, or invoke `.venv\Scripts\python.exe` directly.

Open `http://127.0.0.1:8000` for the app and `http://127.0.0.1:8000/docs` for interactive API documentation.

## Enable a real LLM
Put your own API key in `.env` as `OPENAI_API_KEY=...`, set `OPENAI_MODEL` to a model available to your account, and restart the app. Hosted API usage may cost money. Never commit `.env` or put keys in frontend code. Without a key, the app runs in demo retrieval mode.

## Test
```powershell
pytest -q
```

## Limitations to explain in interviews
- Portfolio demo, not production-ready.
- No live orders, accounts, identity verification, or ticketing integration.
- Uploaded document indexing resets after restart.
- No authentication or rate limiting; do not expose publicly with sensitive documents.
- PDF support requires selectable text, not scanned pages.
- Before production: add authentication, access controls, persistent document indexing, monitoring, evaluation, rate limits, and human escalation workflows.

## Next improvements
1. Add embeddings and semantic search.
2. Add a mock order-status tool with clear test data.
3. Add deployment, logging, CI, and more retrieval/evaluation tests.
