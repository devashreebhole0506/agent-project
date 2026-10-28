from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from threading import Lock

from app.config import settings
from app.tools import calculator, project_lookup, current_time


def build_agent():
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    model = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )

    tools = [
        calculator,
        project_lookup,
        current_time,
    ]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful AI agent. "
            "Use the available tools whenever a request requires "
            "calculation, project information lookup, or time lookup. "
            "Explain the result clearly. "
            "Never claim that a tool succeeded if it failed."
        ),
    )

    return agent


agent = None
_agent_lock = Lock()


def execute_agent(message: str) -> dict:
    global agent
    if agent is None:
        with _agent_lock:
            if agent is None:
                agent = build_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        }
    )

    messages = result.get("messages", [])

    if not messages:
        raise RuntimeError("The agent returned no messages.")

    final_message = messages[-1]

    return {
        "reply": str(final_message.content),
        "message_count": len(messages),
    }
