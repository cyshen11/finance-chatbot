"""RAG Graph"""

from langgraph.graph import START, StateGraph
from components.vector_store import retrieve
from components.generator import generate
from components.utils import State

def build_graph():
  """Build RAG Graph

  Returns:
      Graph (Graph): RAG Graph
  """
  graph_builder = StateGraph(State).add_sequence([retrieve, generate])
  graph_builder.add_edge(START, "retrieve")
  graph = graph_builder.compile()

  return graph