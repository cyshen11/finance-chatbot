from dotenv import load_dotenv
from components.utils import State
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4

# Load environment variables from the .env file
load_dotenv()

def initialize_vector_store():
  embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

  vector_store = Chroma(
    collection_name="docs_embeddings",
    embedding_function=embeddings,
    persist_directory="data/chroma_langchain_db",  
  )
  
  return vector_store

def add_items(vector_store, documents):
  uuids = [str(uuid4()) for _ in range(len(documents))]
  vector_store.add_documents(documents=documents, ids=uuids)

def retrieve(state: State):

  vectorstore = initialize_vector_store()
  
  retriever = vectorstore.as_retriever()

  return {"context": retriever.invoke(state["question"])}

  

  