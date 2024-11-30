"""Vector Store to store and retrieve documents"""

from components.utils import State
from components.document_loader import load_documents
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
import streamlit as st

def initialize_vector_store():
  """Initialize vector store

  Returns:
      vector_store (Chroma): ChromaDB object
  """
  embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

  vector_store = Chroma(
    collection_name="docs_embeddings",
    embedding_function=embeddings,
    persist_directory="data/chroma_langchain_db",  
  )
  
  return vector_store

def add_items(vector_store, documents):
  """Add docs to vector store

  Args:
      vector_store (Chroma)
      documents (list(Document))
  
  """
  uuids = [str(uuid4()) for _ in range(len(documents))] # Generate id
  vector_store.add_documents(documents=documents, ids=uuids)

def retrieve(state: State):
  """Retrieve docs from vector store

  Args:
      state (State): RAG State

  Returns:
      context (object): Retrieved docs
  
  """
  vectorstore = initialize_vector_store()
  retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

  return {"context": retriever.invoke(state["question"])}

def create_vector_store():
  """Re-create vector store

  Returns:
      response (bool): Response to front-end that created vector store successfully
  
  """
  documents = load_documents(st.secrets["DOCUMENT_LIBRARY_ID"], st.secrets["FOLDER_ID"])
  vector_store = initialize_vector_store()
  add_items(vector_store, documents)

  return True

  

  