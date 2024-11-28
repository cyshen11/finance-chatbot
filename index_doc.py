from components.document_loader import load_documents
from components.vector_store import initialize_vector_store, add_items
import os
import streamlit as st

if __name__ == "__main__":
  documents = load_documents(st.secrets["DOCUMENT_LIBRARY_ID"], st.secrets["FOLDER_ID"])
  vector_store = initialize_vector_store()
  add_items(vector_store, documents)
  print('success')
  

  