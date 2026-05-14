```python
import streamlit as st
from difflib import SequenceMatcher

# --- Page config ---
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓")
st.title("WEC College Chatbot 🎓")

# --- Load KB ---
with open("wec_college_database-2.txt", "r") as f:
kb = f.read()

# --- Split KB into Q&A pairs ---
qa_pairs = kb.split("\n\n") # Assumes Q&A separated by double newline

# --- Function to find best match ---
def find_answer(user_query, qa_pairs, threshold=0.4):
best_match = None
best_score = 0

for pair in qa_pairs:
if ": " in pair: # Assuming format "Q: ... A: ..."
question = pair.split("\n")[0]
score = SequenceMatcher(None, user_query.lower(), question.lower()).ratio()

if score > best_score:
best_score = score
best_match = pair

if best_score >= threshold:
return best_match
else:
return "I don't have information about that. Please contact WEC directly."

# --- Session state for chat ---
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

# Get response from database
reply = find_answer(user_input, qa_pairs)

# Show assistant message
st.session_state.messages.append({"role": "assistant", "content": reply})
with st.chat_message("assistant"):
st.write(reply)
```

Key changes: Removed all Gemini API stuff, using simple string matching instead. Just make sure your database file has questions and answers clearly separated. What format is your database currently in?
