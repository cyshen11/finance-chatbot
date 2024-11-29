import streamlit as st
from components.vector_store import create_vector_store
import os

st.title("📄 Index Sharepoint Documents")
create_db = st.button("Index")
if not os.environ["OPENAI_API_KEY"].startswith("sk-"):
    st.warning("Please enter your OpenAI API key!", icon="⚠")

if create_db:
    try:
        create_vector_store()
        st.success("✅ Index documents successfully!")
    except:
        st.error("❌ Index documents fail.")