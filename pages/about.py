"""About page"""

import streamlit as st

# Load the README.md content
with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Display the README content
st.markdown(readme_content, unsafe_allow_html=True)