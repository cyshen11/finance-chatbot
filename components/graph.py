"""RAG Graph"""

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from components.writer import write_query
from components.utils import State

def build_graph():
  """Build RAG Graph

  Returns:
      Graph (Graph): RAG Graph
  """
  memory = MemorySaver()
  graph_builder = StateGraph(State).add_sequence([write_query, execute_query])
  graph_builder.add_edge(START, ["write_query", "execute_query"])
  graph = graph_builder.compile(checkpointer=memory, interrupt_before=["execute_query"])

  return graph