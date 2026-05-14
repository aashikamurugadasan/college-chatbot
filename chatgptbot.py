import streamlit as st
from difflib import SequenceMatcher

# --- Page config ---
st.set_page_config(page_title="WEC Chatbot", page_icon="🎓", layout="centered")

# --- Embedded Database ---
KB = """
COLLEGE_NAME: Women's Engineering College (WEC)
SHORT_NAME: WEC
FORMER_NAME: Women's Polytechnic College, Puducherry
ESTABLISHED: 1988
TYPE: Government Institution
GOVERNED_BY: PIPMATE Society, Govt. of Puducherry
ADMINISTERED_BY: Directorate of Higher & Technical Education
AFFILIATION: Puducherry Technological University (PTU)
APPROVED_BY: AICTE, New Delhi
WEBSITE: www.wec.edu.in
EMAIL: principal@wec.edu.in
PHONE: +91 9842397345
ADDRESS: Airport Road, Lawspet, Puducherry - 605008
PRINCIPAL: Dr. M. Thanigasalam
ADMISSION_BODY: CENTAC (Puducherry)
CENTAC_WEBSITE: www.centacpuducherry.in
BTECH_INTRODUCED_YEAR: 2022-23
TARGET_STUDENTS: Women candidates of UT Puducherry

DEPARTMENTS:
D01: Architectural Assistantship (AA) - B.Tech - 60 seats
D02: Computer Science & Engineering (CSE) - B.Tech - 60 seats
D03: Electrical & Electronics Engineering (EEE) - B.Tech - 60 seats
D04: Electronics & Communication Engineering (ECE) - B.Tech - 60 seats
D05: Information Science & Engineering (ISE) - B.Tech - 60 seats
D06: Commerce (B.Com) - 60 seats - Affiliated to Pondicherry University
D07: Science & Humanities - Supporting Department
D08: Library - Facility

TOTAL SEATS: 360 (300 B.Tech + 60 B.Com)

FEE STRUCTURE:
B.Tech Puducherry Resident: 43,500 INR per year
B.Tech Other State Student: 83,500 INR per year
B.Com Puducherry Resident: 13,500 INR per year
B.Com Other State Student: 28,500 INR per year

CURRICULUM:
Syllabus Body: Puducherry Technological University (PTU)
First Year B.Tech: Common curriculum for all branches
NEP applicable from 2026 batch onwards
Online fee payment available via wec.edu.in

ADMISSION:
Mode: Only through CENTAC (Puducherry)
CENTAC full form: Centralised Admissions Committee
Website: www.centacpuducherry.in
Eligibility: Women candidates of UT Puducherry (priority)
Process: Merit-based via CENTAC counselling

ACADEMIC LINKS:
Academic Calendar: wec.edu.in/academicCalendar.php
Timetable: wec.edu.in/ClassExamSchedule.php
Curriculum & Syllabus: wec.edu.in/curriculum-syllabus.php
Regulation: wec.edu.in/regulation.php
Fee Structure: wec.edu.in/fee_structure.php
AICTE Approvals: wec.edu.in/aicte.php
MoUs & Partnerships: wec.edu.in/mou.php
Grievance Portal: wec.edu.in/grievance.php
News & Events: wec.edu.in/press-news.php

COMMITTEES:
Anti Ragging Committee
Grievance Redressal Committee
Internal Complaint Committee (ICC)
Industry Institute Interaction Cell (III Cell)
Quality Assurance Cell (QAC)
Entrepreneurship Development Cell
Institution Innovation Cell (IIC)
Red Ribbon Club (RRC)
Vishaka Committee

FACILITIES:
Hostel: Available
Library: Available (high-end books)
IoT Lab: Available
Barrier-Free Campus: Yes
Placement Cell: Available
Canva Pro for Students: Available (apply via college portal)
Online Fee Payment: Available
Student Information System: wec.edu.in/wecsisIndex.php

RECENT EVENTS:
Lunova-26: Intra-College Tech Symposium - Registration Open
Smart India Hackathon 2025 (Hardware) - Completed Final Round
GATE-2026 Awareness Class - Conducted
WEC-Zoho MoU Signing Ceremony - Completed
Placement at Eaton / Q-Max - Completed
Placement at Royal Enfield - Completed
Bhoomi Pooja New Laboratory Block - Completed
Kumutham Award - Received

EXTERNAL LINKS:
e-Samadhaan (UGC): samadhaan.ugc.ac.in
Ministry of Education: education.gov.in
NDL (IIT KGP): ndl.iitkgp.ac.in
DigiLocker: digilocker.gov.in
AICTE: aicte-india.org
Virtual Labs: cse19-iiith.vlabs.ac.in
UGC: ugc.ac.in
SWAYAM: swayam.gov.in
Spoken Tutorial: spoken-tutorial.org
NPTEL: nptel.ac.in
"""

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

.main-header {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.main-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: #f9d342;
    letter-spacing: 1px;
    margin-bottom: 0.2rem;
}

.main-header p {
    color: #c9b8f0;
    font-size: 0.95rem;
    margin: 0;
}

.badge {
    display: inline-block;
    background: rgba(249,211,66,0.15);
    border: 1px solid #f9d342;
    color: #f9d342;
    border-radius: 20px;
    padding: 2px 14px;
    font-size: 0.75rem;
    margin-bottom: 1.2rem;
    letter-spacing: 1px;
}

.suggestion-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.suggestion-chip {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.2);
    color: #e0d7ff;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.82rem;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #f9d342, #f5a623);
    color: #1a1a2e;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(249,211,66,0.3);
}

.chat-bubble-bot {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    color: #e8e0ff;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    margin: 8px 0;
    max-width: 85%;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    white-space: pre-line;
}

.bot-label {
    font-size: 0.72rem;
    color: #9b8fc0;
    margin-bottom: 4px;
    letter-spacing: 0.5px;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <div class="badge">🎓 GOVT. INSTITUTION · EST. 1988</div>
    <h1>WEC College Chatbot</h1>
    <p>Women's Engineering College, Puducherry · Ask me anything!</p>
</div>
""", unsafe_allow_html=True)

# --- Suggestion chips ---
st.markdown("""
<div class="suggestion-row">
    <span class="suggestion-chip">📋 Departments offered</span>
    <span class="suggestion-chip">💰 Fee structure</span>
    <span class="suggestion-chip">🏫 How to apply</span>
    <span class="suggestion-chip">📞 Contact info</span>
    <span class="suggestion-chip">🏆 Recent events</span>
</div>
""", unsafe_allow_html=True)

# --- Search function ---
def find_answer(user_query):
    query = user_query.lower()
    lines = KB.strip().splitlines()
    scored = []

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        line_lower = line.lower()
        words = query.split()
        match_count = sum(1 for word in words if len(word) > 2 and word in line_lower)
        seq_score = SequenceMatcher(None, query, line_lower).ratio()
        score = match_count * 0.7 + seq_score * 0.3
        if score > 0:
            scored.append((score, i, line))

    scored.sort(reverse=True)

    if scored and scored[0][0] > 0.15:
        top_idx = scored[0][1]
        start = max(0, top_idx - 1)
        end = min(len(lines), top_idx + 6)
        result_lines = [l for l in lines[start:end] if l.strip()]
        return "\n".join(result_lines)
    else:
        return "I don't have information about that in my database.\n\nFor further help, please contact WEC:\n📧 principal@wec.edu.in\n📞 +91 9842397345\n🌐 www.wec.edu.in"

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-label">🎓 WEC Bot</div><div class="chat-bubble-bot">{msg["content"]}</div>', unsafe_allow_html=True)

# --- Input ---
user_input = st.chat_input("Ask something about WEC College...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble-user">{user_input}</div>', unsafe_allow_html=True)

    reply = find_answer(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f'<div class="bot-label">🎓 WEC Bot</div><div class="chat-bubble-bot">{reply}</div>', unsafe_allow_html=True)