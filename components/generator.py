
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from components.utils import State

# Load environment variables from the .env file
load_dotenv()

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc["text"] for doc in docs)

def generate(state:State):
  llm = ChatOpenAI(model="gpt-4o-mini")
  
  # Define prompt for question-answering
  prompt = hub.pull("rlm/rag-prompt")
  
  docs_content = "\n\n".join(doc["text"] for doc in state["context"])
  
  messages = prompt.invoke({"question": state["question"], "context": docs_content})
  
  response = llm.invoke(messages)
  
  return {"answer": response.content}