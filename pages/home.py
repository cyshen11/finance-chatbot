"""Home page"""

import os
import streamlit as st
from components.graph import ChatBot

st.title("⚡ SQL Chatbot/RAG")

# Set environment variables
openai_api_key = os.environ["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGSMITH"]["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGSMITH"]["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGSMITH"]["LANGCHAIN_PROJECT"]

# Functions
def update_session_state(status):
    st.session_state.chat_history.append({"role": "user", "content": status})
    st.session_state.verification_status = status

def write_chat_message(role, prompt):
    st.chat_message(role).write(prompt)
    st.session_state.chat_history.append({"role": role, "content": prompt})

# Add database info and clear chat button to the sidebar
db_info = """
        This SQLite database consists of 4 tables.
        - companies
        - price_history
        - balance_sheets
        - income_statements
        """ 
st.sidebar.info(db_info)
st.sidebar.button("Clear chat", on_click=lambda: st.session_state.chat_history.clear())

# Initialize chatbot and states
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = ChatBot()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "What can I help with?"}]
if 'verification_status' not in st.session_state:
    st.session_state.verification_status = "New"
if 'sql_query' not in st.session_state:
    st.session_state.sql_query = ""

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat interface
if prompt := st.chat_input("Ask a question about the database"):
    # User ask new query
    if st.session_state.verification_status == "New":
        write_chat_message("user", prompt)
        response = st.session_state.chatbot.run_graph(prompt)

        if response:
            write_chat_message("assistant", response)
            
            # Create buttons
            col1, col2 = st.columns(2)
            col1.button("Run query", key="approve_btn", on_click=update_session_state, args=['Run query'])
            col2.button("Modify", key="modify_btn", on_click=update_session_state, args=['Modify query'])
    
    # User provided query
    elif st.session_state.verification_status == "Modify query" or st.session_state.verification_status == "Query invalid":
        write_chat_message("user", prompt)
        st.session_state.chatbot.update_query(prompt)
        
        try:
            response = st.session_state.chatbot.continue_graph()
            if response:
                write_chat_message("assistant", response)
            st.session_state.verification_status = "New"
        except:
            st.session_state.verification_status = "Query invalid"

# User clicked run query
if st.session_state.verification_status == "Run query":
    response = st.session_state.chatbot.continue_graph()
    if response:
        write_chat_message("assistant", response)
        st.session_state.verification_status = "New"

# User clicked modify query
if st.session_state.verification_status == "Modify query":
    response = "Please provide modified query."
    write_chat_message("assistant", response)

# Query provided by user is invalid
if st.session_state.verification_status == "Query invalid":
    response = "Query is not supported. Please write query that is SQLite3 dialect."
    write_chat_message("assistant", response)
