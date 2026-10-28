# AI Agent API

A FastAPI service that routes questions to an OpenAI-powered LangChain agent. The agent can evaluate arithmetic, look up a small built-in project knowledge base, and report the current time in an IANA timezone.

## Run locally

From this directory, create and activate a virtual environment, install dependencies, and configure the API key:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. `OPENAI_MODEL` defaults to `gpt-4.1-mini` and can be changed there. Start the server with:

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API reference. `GET /health` reports service health and whether a model key is configured. `POST /agent` accepts `{"message":"What is 12 * 8?"}` and returns a reply, message count, and status.

## Notes

- The API key is only needed when calling `/agent`; the service and health route can start without it.
- The calculator accepts numeric arithmetic expressions only. It does not evaluate Python code.
- The project lookup is a small demo knowledge base in `app/tools.py`; update it with project-specific facts as needed.
