from typing_extensions import List, TypedDict

class TextEmbedding:
  def __init__(self, text, embedding, source, page):
      self.text = text
      self.embedding = embedding
      self.source = source
      self.page = page

# Define state for application
class State(TypedDict):
    question: str
    context: List[TextEmbedding]
    answer: str
    source: str