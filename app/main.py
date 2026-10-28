from fastapi import FastAPI, HTTPException
from app.config import settings

from app.agent import execute_agent
from app.schemas import AgentRequest, AgentResponse


app = FastAPI(
    title="AI Agent API",
    version="1.0.0",
    description="A tool-using assistant with arithmetic, project lookup, and timezone tools.",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Agent API",
        "model_configured": bool(settings.openai_api_key),
    }


@app.post("/agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    try:
        result = execute_agent(request.message)

        return AgentResponse(
            reply=result["reply"],
            message_count=result["message_count"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Agent execution failed.",
        ) from exc
