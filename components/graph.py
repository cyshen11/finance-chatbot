"""RAG Graph"""

from langgraph.graph import START, StateGraph
from components.writer import write_query
from components.utils import State

def build_graph():
  """Build RAG Graph

  Returns:
      Graph (Graph): RAG Graph
  """
  graph_builder = StateGraph(State).add_sequence([write_query])
  graph_builder.add_edge(START, "write_query")
  graph = graph_builder.compile()

  return graph