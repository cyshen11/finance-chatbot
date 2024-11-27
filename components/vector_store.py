from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
import time

# Load environment variables from the .env file
load_dotenv()

def insert_docs_to_mongodb(docs_to_insert):
   # Connect to your Atlas cluster
  client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
  collection = client[os.getenv("MONGODB_DB_NAME")][os.getenv("MONGODB_DB_COLLECTION")]
  # Insert documents into the collection
  collection.insert_many(docs_to_insert)

  return collection

def create_vector_index(collection):

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


def store_embeddings(docs_to_insert):
  collection = insert_docs_to_mongodb(docs_to_insert)
  create_vector_index(collection)
  

  