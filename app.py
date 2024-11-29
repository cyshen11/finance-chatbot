__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
from components.graph import build_graph
from components.vector_store import create_vector_store

# Set up session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page):
    st.session_state.current_page = page

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
os.environ["OPENAI_API_KEY"] = openai_api_key

settings = st.sidebar.button("📄 Index Sharepoint Documents")
home = st.sidebar.button("🏠 Home")

if settings:
    navigate("Index Docs")

if home:
    navigate("Home")

# Display the appropriate page based on session state
if st.session_state.current_page == "Home":
    st.title("Finance Chatbot")
    graph = build_graph()

    with st.form("my_form"):
        question = st.text_area(
            "Enter text:",
            "What is the NVIDIA 2025 Q1 Revenue?",
        )
        submitted = st.form_submit_button("Submit")
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            response = graph.invoke({"question": question})
            st.text("Answer")
            st.info(response["answer"])
            st.text("Source")
            st.info(response["source"])

elif st.session_state.current_page == "Index Docs":
    st.title("📄 Index Sharepoint Documents")
    create_db = st.button("Index")
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    if create_db:
        try:
            create_vector_store()
            st.success("✅ Index documents successfully!")
        except:
            st.error("❌ Index documents fail.")

