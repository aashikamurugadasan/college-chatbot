import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="WEC Chatbot", page_icon="🎓")
st.title("🎓 WEC College Chatbot")

# ── Load KB ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_kb():
    with open("wec_college_database-2.txt", "r") as f:
        return f.read()

kb = load_kb()

SYSTEM_PROMPT = f"""
You are WEC chatbot. Answer questions politely and concisely based only on the knowledge base below.
If a question is outside the knowledge base, say you don't have that information.

{kb}
"""

# ── Fresh client every time (no session timeout) ──────────────────────────────
def get_client():
    return genai.Client(api_key="AIzaSyAVOyjzUS2UZMvIOR2gFzUY0QoB-YRAWgI")

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Clear chat button ─────────────────────────────────────────────────────────
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ── Display history ───────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask something about WEC...")

if user_input:
    # ── Input validation ──────────────────────────────────────────────────────
    user_input = user_input.strip()

    if not user_input:
        st.warning("Please type a message before sending.")
        st.stop()

    if len(user_input) > 1000:
        st.warning("Your message is too long. Please keep it under 1000 characters.")
        st.stop()

    if not any(c.isalpha() for c in user_input):
        st.warning("Please enter a valid question with text.")
        st.stop()

    # ── Show user message ─────────────────────────────────────────────────────
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Build history for context
    history = []
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            reply = None
            # Try up to 3 times with a fresh client each attempt
            for attempt in range(3):
                try:
                    client = get_client()
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=history + [types.Content(role="user", parts=[types.Part(text=user_input)])],
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            max_output_tokens=512,
                            temperature=0.3,
                        )
                    )
                    # Validate response before using
                    if response and response.text and response.text.strip():
                        reply = response.text
                        break
                    else:
                        reply = "I couldn't find an answer for that. Please try rephrasing your question."
                        break
                except Exception as e:
                    if attempt == 2:
                        reply = "Sorry, I'm having trouble connecting right now. Please try again."

        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})