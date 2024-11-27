import streamlit as st
from components.graph import build_graph

st.title("Finance Chatbot")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
graph = build_graph()

with st.form("my_form"):
    question = st.text_area(
        "Enter text:",
        "What is the NVIDIA 2025 Q1 Revenue?",
    )
    submitted = st.form_submit_button("Submit")
    # if not openai_api_key.startswith("sk-"):
    #     st.warning("Please enter your OpenAI API key!", icon="⚠")
    # if submitted and openai_api_key.startswith("sk-"):
    if submitted:
        response = graph.invoke({"question": question})
        st.info(response["answer"])
