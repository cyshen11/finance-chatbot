from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv

load_dotenv()

loader = SharePointLoader(document_library_id="YOUR DOCUMENT LIBRARY ID")