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

# Initialize chatbot and states
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": db_info}]
if 'verification_status' not in st.session_state:
    st.session_state.verification_status = "New"
if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ""

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def update_session_state(status):
    st.chat_message("user").write(status)
    st.session_state.chat_history.append({"role": "user", "content": status})
    st.session_state.verification_status = status

# Chat interface
if prompt := st.chat_input("Ask a question about the database"):
    if st.session_state.verification_status == "New":
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        response = st.session_state.chatbot.run_graph(prompt)
        if response:
            st.chat_message("assistant").write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            col1, col2 = st.columns(2)
            col1.button("Run query", key="approve_btn", on_click=update_session_state, args=['Run query'])
            col2.button("Modify", key="modify_btn", on_click=update_session_state, args=['Modify query'])
    
    elif st.session_state.verification_status == "Modify query" or st.session_state.verification_status == "Query invalid":

        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chatbot.update_query(prompt)
        
        try:
            response = st.session_state.chatbot.continue_graph()
            if response:
                st.chat_message("assistant").write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.verification_status = "New"
        except:
            st.session_state.verification_status = "Query invalid"


if st.session_state.verification_status == "Run query":
    response = st.session_state.chatbot.continue_graph()
    if response:
        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.verification_status = "New"

if st.session_state.verification_status == "Modify query":
    response = "Please provide modified query."
    st.chat_message("assistant").write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if st.session_state.verification_status == "Query invalid":
    response = "Query is not supported. Please try different query."
    st.chat_message("assistant").write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
