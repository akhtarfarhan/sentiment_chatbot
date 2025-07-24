from fastapi import FastAPI, HTTPException
from .schemas  import ChatRequest, ChatResponse
from .chat     import respond

app = FastAPI(title="Sentiment-Aware Chatbot")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        answer, sentiment = respond(req.session_id, req.message)
        return ChatResponse(session_id=req.session_id,
                            answer=answer,
                            sentiment=sentiment)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
