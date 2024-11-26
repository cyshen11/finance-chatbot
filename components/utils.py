from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def init_sharepoint_loader():
  loader = SharePointLoader(
    document_library_id=os.getenv("DOCUMENT_LIBRARY_ID"), 
    auth_with_token=True,
    folder_id=os.getenv("FOLDER_ID")
  )
  return loader

def extract_pdf_text(docs):
  extracted_text = {}
  for d in docs:
    extracted_text[d.metadata['source'] + '|' + str(d.metadata['page'])] = d.page_content

  return extracted_text

if __name__ == "__main__":
  sharepoint_loader = init_sharepoint_loader()
  docs = sharepoint_loader.load()
  extracted_text = extract_pdf_text(docs)
  print(extracted_text)