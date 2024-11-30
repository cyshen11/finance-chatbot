"""Streamlit App"""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import os
import streamlit as st

# Dropdown for user to select model
model = st.sidebar.selectbox("Model", ["Google Gemini 1.5 Flash-8B", "OpenAI gpt-4o-mini"])
os.environ["model"] = model

# Initialize to avoid key error
os.environ["OPENAI_API_KEY"] = ""

# Get API keys
os.environ["API_KEY_PROVIDED"] = "y"
if model == "OpenAI gpt-4o-mini":
  openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
  os.environ["OPENAI_API_KEY"] = openai_api_key

  # Check if API key provided
  if not openai_api_key.startswith("sk-"):
      st.sidebar.warning("Please enter your OpenAI API key!", icon="⚠")
      os.environ["API_KEY_PROVIDED"] = "n"
else:
  os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Pages
pg = st.navigation([
  st.Page("pages/home.py", title="Home"), 
  st.Page("pages/index_docs.py", title="Index Docs"), 
  st.Page("pages/about.py", title="About")]
)
pg.run()
