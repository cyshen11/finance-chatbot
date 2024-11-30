"""Generator to generate response based on retrieved docs"""

from langchain import hub
from langchain_openai import ChatOpenAI
from components.utils import State

def generate(state:State):
  """Generate response based on retrieved docs

  Args:
      state (State): RAG State (defined in utils.py)

  Returns:
      Response (Object): Response object contains answer and source
  """

  llm = ChatOpenAI(model="gpt-4o-mini")
  prompt = hub.pull("rlm/rag-prompt")
  
  # Check if no retrieved docs, return no context
  if not state["context"]:
     return {"answer": "no context"}

  # Post-processing retrieved docs
  docs_content = "\n\n".join(doc.page_content for doc in state["context"])
  
  # Get only documents with unique source and page
  unique_documents = []
  seen = set()
  for doc in state["context"]:
    source = doc.metadata.get("source")
    page = doc.metadata.get("page")
    identifier = (source, page)
    if identifier not in seen:
        unique_documents.append(doc)
        seen.add(identifier)

  docs_source = "\n\n".join( 'page:' + str(doc.metadata['page']) + '\nsource:' + doc.metadata['source'] for doc in unique_documents)

  # Generate prompt
  messages = prompt.invoke({"question": state["question"], "context": docs_content})
  
  # Generate answer
  response = llm.invoke(messages)
  
  return {"answer": response.content, "source": docs_source}