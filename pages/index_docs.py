"""Index Docs page"""

import streamlit as st
from components.vector_store import create_vector_store
import os

st.title("📄 Index Sharepoint Documents")
create_db = st.button("Index")

if create_db and os.environ["API_KEY_PROVIDED"] == "y":
    try:
        create_vector_store()
        st.success("✅ Index documents successfully!")
    except:
        st.error("❌ Index documents fail.")