from typing_extensions import List, TypedDict

class TextEmbedding:
  def __init__(self, text, embedding):
      self.text = text
      self.embedding = embedding

# Define state for application
class State(TypedDict):
    question: str
    context: List[TextEmbedding]
    answer: str