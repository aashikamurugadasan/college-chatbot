import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

.chat-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
}

.chat-header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.chat-header p {
    color: #aaa;
    font-size: 0.9rem;
    margin-top: 0.2rem;
}

.stChatMessage {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stChatInputContainer {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <h1>🎓 WEC College Chatbot</h1>
    <p>Women's Engineering College, Puducherry — Ask me anything!</p>
</div>
""", unsafe_allow_html=True)

# ── Embedded Knowledge Base ───────────────────────────────────
WEC_KB = """
WOMEN'S ENGINEERING COLLEGE (WEC) - COMPLETE INFORMATION

=== GENERAL INFO ===
- Full Name: Women's Engineering College (WEC)
- Former Name: Women's Polytechnic College, Puducherry
- Established: 1988
- Type: Government Institution
- Governed by: PIPMATE Society, Govt. of Puducherry
- Administered by: Directorate of Higher & Technical Education
- Affiliation: Puducherry Technological University (PTU)
- Approved by: AICTE, New Delhi
- Website: www.wec.edu.in
- Email: principal@wec.edu.in
- Phone: +91 9842397345
- Address: Airport Road, Lawspet, Puducherry - 605008
- Principal: Dr. M. Thanigasalam
- Admission Body: CENTAC (Centralised Admissions Committee), Puducherry
- Admission Enquiry: www.centacpuducherry.in
- B.Tech Introduced: 2022-23
- Target Students: Women candidates of UT Puducherry

=== DEPARTMENTS ===
1. Architectural Assistantship (AA) - B.Tech - 60 seats
2. Computer Science & Engineering (CSE) - B.Tech - 60 seats
3. Electrical & Electronics Engineering (EEE) - B.Tech - 60 seats
4. Electronics & Communication Engineering (ECE) - B.Tech - 60 seats
5. Information Science & Engineering (ISE) - B.Tech - 60 seats
6. Commerce (B.Com) - 60 seats - Affiliated to Pondicherry University
7. Science & Humanities - Supporting Department
8. Library - Facility

=== TOTAL SEATS ===
- B.Tech (5 departments): 300 seats (60 per department)
- B.Com: 60 seats
- Total: 360 seats

=== FEE STRUCTURE ===
- B.Tech, Puducherry Resident: Rs.43,500/year
- B.Tech, Other State Student: Rs.83,500/year
- B.Com, Puducherry Resident: Rs.13,500/year
- B.Com, Other State Student: Rs.28,500/year
- Online fee payment available via wec.edu.in

=== ADMISSION ===
- Mode: Only through CENTAC (Centralised Admissions Committee)
- CENTAC Website: www.centacpuducherry.in
- Eligibility: Women candidates of UT Puducherry (priority)
- Process: Merit-based via CENTAC counselling
- Documents: As per CENTAC and PTU norms

=== CURRICULUM ===
- Syllabus Body: Puducherry Technological University (PTU)
- First Year B.Tech: Common curriculum for all branches
- NEP applicable from 2026 batch (26th batch) onwards

=== FACILITIES ===
- Hostel: Available
- Library: Available (high-end books)
- IoT Lab: Available
- Barrier-Free Campus: Yes (Ministry of Social Justice funded)
- Placement Cell: Available
- Canva Pro for Students: Available (apply via college portal)
- Online Fee Payment: Available
- Student Information System: wec.edu.in/wecsisIndex.php

=== COMMITTEES ===
1. Anti Ragging Committee
2. Grievance Redressal Committee
3. Internal Complaint Committee (ICC)
4. Industry Institute Interaction Cell (III Cell)
5. Quality Assurance Cell (QAC)
6. Entrepreneurship Development Cell
7. Institution Innovation Cell (IIC)
8. Red Ribbon Club (RRC)
9. Vishaka Committee

=== RECENT EVENTS ===
- Lunova-26: Intra-College Tech Symposium (Registration Open)
- Smart India Hackathon 2025 (Hardware): Completed - Final Round
- GATE-2026 Awareness Class: Conducted
- WEC-Zoho MoU Signing Ceremony: Completed
- Placements at Eaton, Q-Max, Royal Enfield: Completed
- Bhoomi Pooja - New Laboratory Block: Completed
- Kumutham Award: Received

=== IMPORTANT LINKS ===
- Academic Calendar: wec.edu.in/academicCalendar.php
- Timetable: wec.edu.in/ClassExamSchedule.php
- Curriculum & Syllabus: wec.edu.in/curriculum-syllabus.php
- Fee Structure: wec.edu.in/fee_structure.php
- Grievance Portal: wec.edu.in/grievance.php
- News & Events: wec.edu.in/press-news.php
- SWAYAM: swayam.gov.in
- NPTEL: nptel.ac.in
"""

# ── System Prompt ─────────────────────────────────────────────
SYSTEM_PROMPT = f"""You are Veda, the friendly AI assistant for Women's Engineering College (WEC), Puducherry.

Your personality:
- Warm, cheerful, and conversational — talk like a helpful senior student, not a robot
- Use simple, clear language
- Add light emojis occasionally to make responses friendly (but don't overdo it)
- Keep answers concise but complete
- If someone seems confused, reassure them and guide them gently

Your knowledge base (ONLY use this to answer — do not make up anything):
{WEC_KB}

If a question is outside the knowledge base, say:
"I don't have that information right now. Please contact WEC directly at principal@wec.edu.in or call +91 9842397345 😊"
"""

# ── Groq Client ───────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ── Session State ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Quick Question Buttons ────────────────────────────────────
st.markdown("**Quick questions:**")
cols = st.columns(3)
quick_questions = [
    "What departments are offered?",
    "What is the fee structure?",
    "How do I apply for admission?",
    "What facilities does WEC have?",
    "Who is the Principal?",
    "Recent events at WEC?",
]
for i, q in enumerate(quick_questions):
    if cols[i % 3].button(q, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q})
        st.rerun()

st.divider()

# ── Display Chat History ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Chat Input ────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about WEC... 🎓")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                max_tokens=1000,
            )
            reply = response.choices[0].message.content

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})