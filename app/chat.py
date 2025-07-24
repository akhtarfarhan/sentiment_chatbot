# app/chat.py  (final, no LLMChain)

from langchain_community.chat_models import ChatOllama   # ← works on LangChain 0.2+
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from .sentiment import get_sentiment
from .memory    import get_memory

LLM = ChatOllama(model="mistral", temperature=0.7)

SYSTEM_TEMPLATE = """
You are a helpful AI assistant.
The user's current sentiment is {sentiment}.
• If the sentiment is NEGATIVE, reply with warmth and encouragement.
• If the sentiment is POSITIVE, mirror their enthusiasm.
Always keep answers concise and clear.
""".strip()

def respond(session_id: str, user_msg: str) -> tuple[str, str]:
    """Return (assistant_reply, detected_sentiment)."""
    sentiment = get_sentiment(user_msg)
    memory: ConversationBufferMemory = get_memory(session_id)

    # ---- build message list ----
    messages = [SystemMessage(content=SYSTEM_TEMPLATE.format(sentiment=sentiment))]
    messages.extend(memory.chat_memory.messages)   # past turns
    messages.append(HumanMessage(content=user_msg))

    # ---- call model ----
    answer_msg: AIMessage = LLM.invoke(messages)
    answer = answer_msg.content.strip()

    # ---- save turn to memory ----
    memory.chat_memory.add_user_message(user_msg)
    memory.chat_memory.add_ai_message(answer)

    return answer, sentiment
