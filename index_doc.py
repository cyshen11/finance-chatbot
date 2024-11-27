from components.document_loader import load_documents
from components.embedder import embed_documents
from components.vector_store import store_embeddings
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

if __name__ == "__main__":
  docs = load_documents(os.getenv("DOCUMENT_LIBRARY_ID"), os.getenv("FOLDER_ID"))
  embeddings = embed_documents(docs)
  store_embeddings(embeddings)
  print('success')
  

  