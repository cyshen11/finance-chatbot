"""Home page"""

import os
import streamlit as st
from components.graph import ChatBot
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

# Initialize chat history
# st.chat_message("assistant").write(db_info)

# Initialize chatbot and states
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": db_info}]
if 'verification_status' not in st.session_state:
    st.session_state.verification_status = False
if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ""

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def update_session_state(status):
    # st.chat_message("assistant").write(status)
    st.session_state.chat_history.append({"role": "user", "content": status})
    st.session_state.verification_status = status

# Chat interface
if prompt := st.chat_input("Ask a question about the database"):
    st.chat_message("user").write(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    response = st.session_state.chatbot.run_graph(prompt)
    if response:
        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        col1, col2, col3 = st.columns(3)
        
        approve = col1.button("Run query", key="approve_btn", on_click=update_session_state, args=['Run query'])
        col2.button("Modify", key="modify_btn")
        col3.button("Reject", key="reject_btn")

if st.session_state.verification_status == "Run query":
    response = st.session_state.chatbot.continue_graph()
    if response:
        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})