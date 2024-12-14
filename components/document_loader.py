"""Document loader to load documents"""

from langchain_community.document_loaders.sharepoint import SharePointLoader
import warnings
import streamlit as st
import json
from pathlib import Path
import os

# Get parameters
O365_CLIENT_ID=st.secrets["O365_CLIENT_ID"]
O365_CLIENT_SECRET=st.secrets["O365_CLIENT_SECRET"]
O365_TOKEN=dict(st.secrets["O365_TOKEN"])

def init_sharepoint_loader(document_library_id, folder_id):
  """Initialize SharePoint document loaders

  Args:
      document_library_id (str): SharePoint document library ID (default is None)
      folder_id (str): SharePoint folder ID (default is None)

  Returns:
      DocumentLoader: LangChain document loaders object
  """

  directory_path = Path.home() / ".credentials"

  # Check if dir exist
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)

  # Write O365 token into text file 
  with open(directory_path / "o365_token.txt", 'w') as f:
    json.dump(O365_TOKEN, f)

  # Initialize document loader
  loader = SharePointLoader(
    document_library_id=document_library_id, 
    auth_with_token=True,
    folder_id=folder_id
  )

  return loader

def load_documents(document_library_id, folder_id):
  """Load docs from SharePoint

  Args:
      document_library_id (str): SharePoint document library ID (default is None)
      folder_id (str): SharePoint folder ID (default is None)

  Returns:
      Array of LandChain Doc objects (arr)
  """


  sharepoint_loader = init_sharepoint_loader(document_library_id, folder_id)

  # supress warnings for empty PDF page
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    documents = sharepoint_loader.load()

  return documents
  

  