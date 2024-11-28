from langchain_community.document_loaders.sharepoint import SharePointLoader
import warnings
import streamlit as st

O365_CLIENT_ID=st.secrets["O365_CLIENT_ID"]
O365_CLIENT_SECRET=st.secrets["O365_CLIENT_SECRET"]

def init_sharepoint_loader(document_library_id, folder_id):

  try:
    loader = SharePointLoader(
      document_library_id=document_library_id, 
      auth_with_token=True,
      folder_id=folder_id
    )
  except:
    loader = SharePointLoader(
      document_library_id=document_library_id, 
      auth_with_token=False,
      folder_id=folder_id
    )

  return loader

def load_documents(document_library_id, folder_id):
  sharepoint_loader = init_sharepoint_loader(document_library_id, folder_id)
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    documents = sharepoint_loader.load()

  return documents
  

  