import streamlit as st
import re
from pathlib import Path

st.set_page_config(
    page_title="Bahria University Admission Assistant",
    page_icon="🎓"
)

def load_faq():
    faq_path = Path(__file__).parent / "faq.txt"

    if not faq_path.exists():
        return []

    content = faq_path.read_text(encoding="utf-8")
    entries = []
    current = {}

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("Question:"):
            if current.get("question") and current.get("answer"):
                entries.append(current)

            current = {
                "question": line.replace("Question:", "", 1).strip()
            }

        elif line.startswith("Keywords:"):
            current["keywords"] = [
                word.strip().lower()
                for word in line.replace("Keywords:", "", 1).split(",")
            ]

        elif line.startswith("Answer:"):
            current["answer"] = line.replace("Answer:", "", 1).strip()

    if current.get("question") and current.get("answer"):
        entries.append(current)

    return entries


def find_answer(user_question, faq):

    question = user_question.lower().strip()

    # Greeting responses
    greetings = [
        "hi", "hello", "hey", "hii", "hiii",
        "salam", "assalamualaikum",
        "assalamu alaikum", "good morning",
        "good afternoon", "good evening"
    ]

    if question in greetings:
        return (
            "Assalamualaikum! Welcome to Bahria University's "
            "H-11 Campus Admission Assistant. 🎓 "
            "How can I help you today?"
        )

    # Goodbye responses
    goodbyes = ["bye", "goodbye", "see you", "allah hafiz"]

    if question in goodbyes:
        return "Allah Hafiz! Thank you for using Bahria University's Admission Assistant."

    # Thank you responses
    thanks = ["thanks", "thank you", "thankyou", "thx"]

    if question in thanks:
        return "You're welcome! Feel free to ask if you have more questions."

    # Match keywords from FAQ
    best_answer = None
    highest_score = 0

    for entry in faq:
        score = 0

        for keyword in entry.get("keywords", []):
            if keyword and re.search(
                r"\b" + re.escape(keyword) + r"\b",
                question
            ):
                score += 1

        if score > highest_score:
            highest_score = score
            best_answer = entry["answer"]

    if highest_score > 0:
        return best_answer

    return (
        "Sorry, I couldn't find a verified answer to that question. "
        "Please contact Bahria University's H-11 Admissions Office "
        "at adadmission.h11@bahria.edu.pk or 051-9259493."
    )


# Main chatbot interface

st.title("🎓 Bahria University")
st.subheader("H-11 Campus Admission Assistant")

st.write(
    "Ask me about admissions, eligibility, programs, "
    "fees, scholarships and university facilities."
)

st.info(
    "This is a student-developed chatbot, not an official "
    "Bahria University service."
)

faq = load_faq()

if not faq:
    st.error("Unable to load the knowledge base. Please try again.")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_question = st.chat_input("Ask your question here...")

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    answer = find_answer(user_question, faq)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
