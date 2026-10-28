from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class AgentResponse(BaseModel):
    reply: str
    message_count: int
    status: str = "success"