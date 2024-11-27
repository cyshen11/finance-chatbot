from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from the .env file
load_dotenv()

# Define a function to generate embeddings
def get_embedding(text):
   """Generates vector embeddings for the given text."""
   model = os.getenv("EMBEDDING_MODEL")
   openai_client = OpenAI()
   embedding = openai_client.embeddings.create(input = [text], model=model).data[0].embedding
   return embedding

def embed_documents(documents):
   # Prepare documents for insertion
  docs_to_insert = [{
      "text": doc.page_content,
      "embedding": get_embedding(doc.page_content),
      # "source": doc.metadata['source'],
      # "page": doc.metadata['page']
  } for doc in documents]

  return docs_to_insert
  

  