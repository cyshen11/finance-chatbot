"""Home page"""

import os
import streamlit as st
from components.graph import build_graph

st.title("⚡ SQL Chatbot/RAG")

graph = build_graph()

openai_api_key = os.environ["OPENAI_API_KEY"]

st.markdown(
    """
        This database consists of 4 tables.
        - companies
        - price_history
        - balance_sheets
        - income_statements
    """
)

with st.form("my_form"):
  question = st.text_area(
      "Enter text:",
      "What is the NVIDIA 2024 Q3 Revenue?",
  )
  submitted = st.form_submit_button("Submit")
  
  if submitted and os.environ["API_KEY_PROVIDED"] == "y":
      response = graph.invoke({"question": question})
      st.markdown("### Answer")
      st.text(response["answer"])
      st.markdown("### Source")
      st.markdown(response["source"])