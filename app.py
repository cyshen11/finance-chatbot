import streamlit as st
from components.vector_store import retrieve

st.title("Finance Chatbot")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What is the NVIDIA 2024 Q1 Revenue?",
    )
    submitted = st.form_submit_button("Submit")
    # if not openai_api_key.startswith("sk-"):
    #     st.warning("Please enter your OpenAI API key!", icon="⚠")
    # if submitted and openai_api_key.startswith("sk-"):
    if submitted:
        st.info(retrieve(text))
