from langchain.memory import ConversationBufferMemory

_memories: dict[str, ConversationBufferMemory] = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    """Return (or create) a ConversationBufferMemory for this chat."""
    if session_id not in _memories:
        _memories[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
    return _memories[session_id]
