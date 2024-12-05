"""Home page"""

import os
import streamlit as st
from components.graph import build_graph, run_graph
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

st.title("⚡ SQL Chatbot/RAG")

# Set environment variables
openai_api_key = os.environ["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGSMITH"]["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGSMITH"]["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGSMITH"]["LANGCHAIN_PROJECT"]

db_info = """
        This database consists of 4 tables.
        - companies
        - price_history
        - balance_sheets
        - income_statements
    """ 

def record_user_message(prompt):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

def record_assistant_message(response):
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": db_info}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

graph = build_graph()

# React to user input
if prompt := st.chat_input("What is up?"):
    record_user_message(prompt)
    st.write(run_graph(graph, prompt, "write_query"))
    response = f"Please advise whether to run the query (y/n)"
    record_assistant_message(response)

    if prompt == "y":
        record_user_message(prompt)
        st.write(run_graph(graph, prompt, "generate_answer"))
        response = f""
        record_assistant_message(response)