import streamlit as st
from difflib import SequenceMatcher

# --- Page config ---
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓")
st.title("WEC College Chatbot 🎓")

# --- Load KB ---
with open("wec_college_database-2.txt", "r") as f:
    kb = f.read()

# --- Split KB into sections ---
sections = [s.strip() for s in kb.split("---") if s.strip()]

# --- Keyword search function ---
def find_answer(user_query):
    query = user_query.lower()
    best_section = None
    best_score = 0

    for section in sections:
        # Score based on keyword overlap
        section_lower = section.lower()
        words = query.split()
        match_count = sum(1 for word in words if word in section_lower)
        seq_score = SequenceMatcher(None, query, section_lower[:200]).ratio()
        score = match_count * 0.6 + seq_score * 0.4

        if score > best_score:
            best_score = score
            best_section = section

    if best_score > 0.2 and best_section:
        # Clean up and return relevant lines only
        lines = best_section.strip().splitlines()
        relevant = [l.strip() for l in lines if l.strip() and not l.startswith("=") and not l.startswith("-")]
        return "\n".join(relevant[:15])  # Return up to 15 lines
    else:
        return "I don't have information about that. Please contact WEC at principal@wec.edu.in or call +91 9842397345."

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Input ---
user_input = st.chat_input("Ask something about WEC...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    reply = find_answer(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)