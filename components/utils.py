from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel  
from langchain_community.document_loaders.sharepoint import SharePointLoader
from dotenv import load_dotenv
import os
import tiktoken
import warnings

# Load environment variables from the .env file
load_dotenv()

def init_sharepoint_loader():
  loader = SharePointLoader(
    document_library_id=os.getenv("DOCUMENT_LIBRARY_ID"), 
    auth_with_token=True,
    folder_id=os.getenv("FOLDER_ID")
  )
  return loader

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

def extract_pdf_text(docs):
  extracted_text = {}
  for d in docs:
    extracted_text[d.metadata['source'] + '|' + str(d.metadata['page'])] = d.page_content

  return extracted_text

if __name__ == "__main__":
  #### INDEXING ####

  # Load Documents
  sharepoint_loader = init_sharepoint_loader()
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    docs = sharepoint_loader.load()

  # Embed
  vectorstore = Chroma.from_documents(documents=docs, 
                                    embedding=OpenAIEmbeddings())
  retriever = vectorstore.as_retriever()

  #### RETRIEVAL and GENERATION ####

  # Prompt
  prompt = hub.pull("rlm/rag-prompt")

  # LLM
  llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

  # Post-processing
  def format_docs(docs):
      return "\n\n".join(doc.page_content for doc in docs)

  # Chain
  rag_chain_from_docs = (
      RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
      | prompt
      | llm
      | StrOutputParser()
  )

  rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
  ).assign(answer=rag_chain_from_docs)

  # Question
  answer = rag_chain_with_source.invoke("What is Alphabet Q1 FY24 revenue?")
  print(answer)

  