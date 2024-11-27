import streamlit as st
from components.graph import build_graph
from components.vector_store import create_vector_store

# Set up session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def navigate(page):
    st.session_state.current_page = page

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
settings = st.sidebar.button("⚙️ Settings")
home = st.sidebar.button("🏠 Home")

if settings:
    navigate("Settings")

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
        # if not openai_api_key.startswith("sk-"):
        #     st.warning("Please enter your OpenAI API key!", icon="⚠")
        # if submitted and openai_api_key.startswith("sk-"):
        if submitted:
            response = graph.invoke({"question": question})
            st.text("Answer")
            st.info(response["answer"])
            st.text("Source")
            st.info(response["source"])

elif st.session_state.current_page == "Settings":
    st.title("Settings Page")
    if st.button("Create database"):
        try:
            create_vector_store()
            st.success("✅ Database created successfully!")
        except:
            st.error("❌ Database creation failed.")

