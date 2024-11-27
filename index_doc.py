from components.document_loader import load_documents
from components.vector_store import initialize_vector_store, add_items
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from the .env file
load_dotenv()

if __name__ == "__main__":
  documents = load_documents(os.getenv("DOCUMENT_LIBRARY_ID"), os.getenv("FOLDER_ID"))
  vector_store = initialize_vector_store()
  add_items(vector_store, documents)
  print('success')
  

  