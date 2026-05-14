import streamlit as st
from google import genai

# --- Page config ---
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓")
st.title("WEC College Chatbot 🎓")

# --- Load KB ---
with open("wec_college_database-2.txt", "r") as f:
    kb = f.read()

# --- System prompt ---
system_prompt = f"""
you are wec chatbot your job is to provide answers to the questions asked by customers, 
so you answer them in polite, if there is any question out of the kb say you did not have that info, only refer the kb and provide the response,

{kb}
"""

# --- Gemini client ---
API_KEY = "AIzaSyAVOyjzUS2UZMvIOR2gFzUY0QoB-YRAWgI"   # <-- paste your key here
client = genai.Client(api_key=API_KEY)

# --- Session state for chat ---
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_prompt}
    )
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Input ---
user_input = st.chat_input("Ask something about WEC...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get response
    response = st.session_state.chat.send_message(user_input)
    reply = response.text

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)