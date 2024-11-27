from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv
import os
import tiktoken
import warnings
from openai import OpenAI
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import time

# Load environment variables from the .env file
load_dotenv()

def init_sharepoint_loader():
  loader = SharePointLoader(
    document_library_id=os.getenv("DOCUMENT_LIBRARY_ID"), 
    auth_with_token=True,
    folder_id=os.getenv("FOLDER_ID")
  )
  return loader

# Define a function to generate embeddings
def get_embedding(text):
   """Generates vector embeddings for the given text."""
   model = "text-embedding-3-small"
   openai_client = OpenAI()
   embedding = openai_client.embeddings.create(input = [text], model=model).data[0].embedding
   return embedding

def convert_docs_to_embeddings(documents):
   # Prepare documents for insertion
  docs_to_insert = [{
      "text": doc.page_content,
      "embedding": get_embedding(doc.page_content)
  } for doc in documents]

  return docs_to_insert

def insert_docs_to_mongodb(docs_to_insert):
   # Connect to your Atlas cluster
  client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
  collection = client[os.getenv("MONGODB_DB_NAME")][os.getenv("MONGODB_DB_COLLECTION")]
  # Insert documents into the collection
  result = collection.insert_many(docs_to_insert)

  return result

def create_vector_index():
  # Connect to your Atlas cluster
  client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
  collection = client[os.getenv("MONGODB_DB_NAME")][os.getenv("MONGODB_DB_COLLECTION")]

  # Create your index model, then create the search index
  index_name="vector_index"
  search_index_model = SearchIndexModel(
    definition = {
      "fields": [
        {
          "type": "vector",
          "numDimensions": 1536,
          "path": "embedding",
          "similarity": "cosine"
        }
      ]
    },
    name = index_name,
    type = "vectorSearch"
  )
  collection.create_search_index(model=search_index_model)

  # Wait for initial sync to complete
  print("Polling to check if the index is ready. This may take up to a minute.")
  predicate=None
  if predicate is None:
    predicate = lambda index: index.get("queryable") is True
  while True:
    indices = list(collection.list_search_indexes(index_name))
    if len(indices) and predicate(indices[0]):
        break
    time.sleep(5)
  print(index_name + " is ready for querying.")

def num_tokens_from_string(doc: str) -> int:
    # Initialize the tokenizer for a specific model (e.g., OpenAI GPT-3.5-turbo)
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Tokenize the document's content
    tokens = tokenizer.encode(doc.page_content)

    # Count the tokens
    num_tokens = len(tokens)

    return num_tokens

def split_docs(docs):
  text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
      chunk_size=500, chunk_overlap=0
  )
  doc_splits = text_splitter.split_documents(docs)
  return doc_splits



if __name__ == "__main__":
  #### INDEXING ####

  # Load Documents
  sharepoint_loader = init_sharepoint_loader()
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    documents = sharepoint_loader.load()

  # Embed
  docs_to_insert = convert_docs_to_embeddings(documents)

  # Store in MongoDB
  result = insert_docs_to_mongodb(docs_to_insert)

  # Create Atlas Vector Search index
  create_vector_index()
  

  