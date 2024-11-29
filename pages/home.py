import os
import streamlit as st
from components.graph import build_graph

st.title("🤖 Sharepoint Chatbot/RAG")
graph = build_graph()

openai_api_key = os.environ["OPENAI_API_KEY"]

url = "https://vincentcheng659.sharepoint.com/:f:/s/LLM/Epu633cK57BOuois5EdkmagB0XdbZaYMzGPCPZ-K3vRf1Q"
st.markdown(
   "Please ask questions based on the documents in this [Sharepoint folder](%s)" % url,
    unsafe_allow_html=False
)

with st.form("my_form"):
  question = st.text_area(
      "Enter text:",
      "What is the NVIDIA 2025 Q1 Revenue?",
  )
  submitted = st.form_submit_button("Submit")
  if not openai_api_key.startswith("sk-"):
      st.warning("Please enter your OpenAI API key!", icon="⚠")
  if submitted and openai_api_key.startswith("sk-"):
      response = graph.invoke({"question": question})
      st.text("Answer")
      st.info(response["answer"])
      st.text("Source")
      st.info(response["source"])