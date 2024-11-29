__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st

# Widgets shared by all the pages
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
os.environ["OPENAI_API_KEY"] = openai_api_key

pg = st.navigation([
  st.Page("pages/home.py", title="Home"), 
  st.Page("pages/index_docs.py", title="Index Docs"), 
  st.Page("pages/about.py", title="About")]
)
pg.run()
