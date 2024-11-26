from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def auth_sharepoint():
  loader = SharePointLoader(document_library_id=os.getenv("DOCUMENT_LIBRARY_ID"), auth_with_token=True)

if __name__ == "__main__":
  auth_sharepoint()