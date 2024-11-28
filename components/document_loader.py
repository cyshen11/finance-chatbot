from langchain_community.document_loaders.sharepoint import SharePointLoader
import warnings
import streamlit as st
import json
from O365 import Account

O365_CLIENT_ID=st.secrets["O365_CLIENT_ID"]
O365_CLIENT_SECRET=st.secrets["O365_CLIENT_SECRET"]
O365_TOKEN=json.loads(st.secrets["O365_TOKEN"])

def init_sharepoint_loader(document_library_id, folder_id):

  # Initialize O365 Account with the token
  credentials = (None, None)  # No client ID/secret needed for token-based auth
  account = Account(credentials, token_backend=None)
  account.connection.token = O365_TOKEN

  # Refresh the token if needed (optional)
  if not account.is_authenticated:
      account.connection.refresh_token()

  # Check if authentication was successful
  if not account.is_authenticated:
      raise ValueError("Failed to authenticate with the provided O365 token")

  loader = SharePointLoader(
    document_library_id=document_library_id, 
    account=account,
    folder_id=folder_id
  )

  return loader

def load_documents(document_library_id, folder_id):
  sharepoint_loader = init_sharepoint_loader(document_library_id, folder_id)
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    documents = sharepoint_loader.load()

  return documents
  

  