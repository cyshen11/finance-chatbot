from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def init_sharepoint_loader():
  loader = SharePointLoader(
    document_library_id=os.getenv("DOCUMENT_LIBRARY_ID"), 
    auth_with_token=True,
    folder_path=os.getenv("FOLDER_PATH")
  )
  return loader

if __name__ == "__main__":
  sharepoint_loader = init_sharepoint_loader()
  docs = sharepoint_loader.load()
  print(docs)