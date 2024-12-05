"""Home page"""

import os
import streamlit as st
from components.graph import build_graph, graph_write_query
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

st.title("⚡ SQL Chatbot/RAG")

# Set environment variables
openai_api_key = os.environ["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGSMITH"]["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGSMITH"]["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGSMITH"]["LANGCHAIN_PROJECT"]

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
    graph = build_graph()
    st.write(graph_write_query(graph, question))