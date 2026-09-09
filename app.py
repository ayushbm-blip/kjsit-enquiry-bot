# app.py
import streamlit as st
from rag_engine import get_answer, initialize

st.set_page_config(page_title="KJSIT Enquiry Bot", page_icon="🎓")
st.title("🎓 KJSIT College Enquiry Assistant")
st.caption("Ask me anything about admissions, fees, courses, placements, and more — in English, Hindi, Marathi, or Gujarati.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.spinner("Loading knowledge base... (first load may take a minute)"):
        try:
            initialize()
            st.session_state.init_error = None
        except Exception as e:
            st.session_state.init_error = str(e)

if st.session_state.get("init_error"):
    st.error(
        "Could not start the assistant. This is usually because the "
        "GROQ_API_KEY environment variable is not set, or the data/ "
        "folder is missing .txt files.\n\n"
        f"Details: {st.session_state.init_error}"
    )
    st.stop()

st.write("**Try asking:**")
example_cols = st.columns(3)
example_questions = [
    "What is the total fee for Open category students?",
    "What documents do I need for admission?",
    "What subjects are in Semester 3?",
]
clicked_example = None
for col, q in zip(example_cols, example_questions):
    if col.button(q):
        clicked_example = q

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Type your question here...") or clicked_example

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_answer(question)
            except Exception:
                answer = "Sorry, I couldn't process that. Please try rephrasing your question."
           st.markdown(answer, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})