"""Home page"""

import os
import streamlit as st
from components.graph import run_graph

st.title("⚡ SQL Chatbot/RAG")

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
      "What company data is available?",
  )
  submitted = st.form_submit_button("Submit")
  
  if submitted and os.environ["API_KEY_PROVIDED"] == "y":
    #   response = graph.invoke({"question": question})
    # #   st.markdown("### Answer")
    # #   st.text(response["answer"])
    #   st.markdown("### Query")
    #   st.markdown(response['query'])
    st.write_stream(run_graph(question))