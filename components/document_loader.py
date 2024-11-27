from langchain_community.document_loaders.sharepoint import SharePointLoader
import warnings

def init_sharepoint_loader(document_library_id, folder_id):
  loader = SharePointLoader(
    document_library_id=document_library_id, 
    auth_with_token=True,
    folder_id=folder_id
  )
  return loader

def load_documents(document_library_id, folder_id):
  sharepoint_loader = init_sharepoint_loader(document_library_id, folder_id)
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    documents = sharepoint_loader.load()

  return documents
  

  