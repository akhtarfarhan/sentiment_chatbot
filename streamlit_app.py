# streamlit_app.py
import uuid, requests, streamlit as st

# --- sidebar settings ----------------------------------
sid = st.sidebar.text_input("Session ID", value=uuid.uuid4().hex)
api = st.sidebar.text_input("FastAPI URL", value="http://127.0.0.1:8000/chat")

st.title("📊  Sentiment-Aware Chatbot")

# keep chat log in Streamlit session
if "log" not in st.session_state:
    st.session_state.log = []

# --- send user message ---------------------------------
msg = st.chat_input(placeholder="Type here…")
if msg:
    try:
        r = requests.post(api,
                          json={"session_id": sid, "message": msg},
                          timeout=120).json()
        st.session_state.log += [("user", msg),
                                 ("bot",  f"{r['answer']}  "
                                          f"_(sentiment = {r['sentiment']})_")]
    except Exception as e:
        st.error(f"API call failed: {e}")

# --- replay the conversation ---------------------------
for role, text in st.session_state.log:
    st.chat_message(role).markdown(text)
