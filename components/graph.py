"""RAG Graph"""

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from components.writer import write_query
from components.executor import execute_query
from components.utils import State
import json

def build_graph():
  """Build RAG Graph

  Returns:
      Graph (Graph): RAG Graph
  """
  memory = MemorySaver()
  graph_builder = StateGraph(State).add_sequence([write_query, execute_query])
  graph_builder.add_edge(START, "write_query")
  graph = graph_builder.compile(checkpointer=memory, interrupt_before=["execute_query"])

  return graph

def graph_write_query(graph, question):
  config = {"configurable": {"thread_id": "1"}}

  for step in graph.stream(
      {"question": question},
      config,
      stream_mode="updates",
  ):
      yield(step)
