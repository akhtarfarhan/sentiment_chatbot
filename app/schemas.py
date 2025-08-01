from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message:    str

class ChatResponse(BaseModel):
    session_id: str
    answer:     str
    sentiment:  str   # POSITIVE | NEGATIVE | NEUTRAL
