"""Home page"""

import os
import streamlit as st
from components.graph import build_graph
from components.vector_store import check_vector_store_exist

st.title("🤖 SharePoint Chatbot/RAG")

graph = build_graph()
check_vector_store_exist()

openai_api_key = os.environ["OPENAI_API_KEY"]

url = st.secrets["SHAREPOINT_URL"]
st.markdown(
   "Please ask questions based on the documents in this [Sharepoint folder](%s)" % url,
    unsafe_allow_html=False
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