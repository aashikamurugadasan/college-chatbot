import streamlit as st
from google import genai
from tenacity import retry, wait_exponential, stop_after_attempt
from google.genai.errors import ServerError

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓")
st.title("🎓 WEC College Chatbot")

# ── Load KB ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_kb():
    with open("wec_college_database-2.txt", "r") as f:
        return f.read()

kb = load_kb()

# ── Gemini client ─────────────────────────────────────────────────────────────
API_KEY = "AIzaSyAVOyjzUS2UZMvIOR2gFzUY0QoB-YRAWgI"
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = f"""
You are WEC chatbot. Your job is to provide answers to questions asked by users.
Answer politely. If a question is outside the knowledge base, say you don't have that information.
Only refer to the knowledge base below and provide responses based on it.

{kb}
"""

# ── Chat session (persisted in session_state) ─────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Retry wrapper ─────────────────────────────────────────────────────────────
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5), reraise=True)
def send_message_with_retry(chat_session, message):
    try:
        return chat_session.send_message(message)
    except ServerError as e:
        print(f"Caught ServerError, retrying...: {e}")
        raise

# ── Display history ───────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask something about WEC...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = send_message_with_retry(st.session_state.chat, user_input)
                reply = response.text
            except Exception as e:
                reply = f"Sorry, something went wrong: {e}"
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})