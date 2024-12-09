"""RAG Graph"""

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from components.writer import write_query
from components.executor import execute_query
from components.generator import generate_answer
from components.utils import State
import streamlit as st
import ast

class ChatBot:
    """ChatBot

    Attrs:
        graph (StateGraph): Langgraph graph 
        config (dict): Langgraph config

    Methods:
        build_graph: Build the graph
        run_graph: Run the graph with a question
        continue_graph: Continue the graph
        update_query: Update the query
        string_tuples_to_markdown_table: Convert string to markdown table
        get_headers_from_sql: Get headers from SQL query
    """
    def __init__(self):
        self.graph = self.build_graph()
        self.config = {"configurable": {"thread_id": "1"}}
        
    def build_graph(self):
        memory = MemorySaver()
        
        # Define the graph builder
        graph_builder = StateGraph(State).add_sequence(
            [write_query, execute_query, generate_answer]
        )
        graph_builder.add_edge(START, "write_query")
        
        graph = graph_builder.compile(
            checkpointer=memory,
            interrupt_before=["execute_query"]
        )

        return graph
    
    def run_graph(self, question: str):
        query = ""
        # Run graph
        for step in self.graph.stream(
            {"question": question},
            self.config,
            stream_mode="updates",
        ):
            # Get query
            if "write_query" in step:
                query = step["write_query"]["query"]
                st.session_state.sql_query = query
                
        content = f"Generated SQL query:\n\n`{query}`\n\n"
        return content
        
    def continue_graph(self):
        query, response, result, answer = "", "", "", ""
        for step in self.graph.stream(
              None,
              self.config,
              stream_mode="updates",
          ):
              # Get result and answer
              if "execute_query" in step:
                  result = step["execute_query"]["result"]
              if "generate_answer" in step:
                  answer = step["generate_answer"]["answer"]

        query = self.graph.get_state(self.config).values["query"]

        response += f"Result:\n{self.string_tuples_to_markdown_table(query, result)}\n\n"
        response += f"Answer:\n{answer}\n\n"
        return response
    
    def update_query(self, query: str):
        self.graph.update_state(self.config, {"query": query}, as_node="write_query")
    
    def string_tuples_to_markdown_table(self, query, data_string):
      # Convert string to list of tuples using eval
      # Remove the outer quotes first
      data_string = data_string.strip('"\'')
      data = ast.literal_eval(data_string)
      
      # Define headers
      headers = self.extract_sql_headers(query)
      
      # Create header row with alignment
      markdown = "| " + " | ".join(headers) + " |\n"
      # Create alignment row (centered alignment)
      markdown += "|" + "|".join([":---:"]*len(headers)) + "|\n"
      
      # Add data rows
      for row in data:
          markdown += "| " + " | ".join(str(item) for item in row) + " |\n"
          
      return markdown
    
    def extract_sql_headers(self, sql_query: str) -> list:
      """
      Extract column headers from a SQL SELECT query, handling aliases and functions.
      
      Args:
          sql_query (str): The SQL query to parse
          
      Returns:
          list: List of column headers
      """
      # Get the SELECT clause (everything between SELECT and FROM)
      try:
          select_clause = sql_query.upper().split('FROM')[0].replace('SELECT', '').strip()
      except IndexError:
          return []

      # Split the columns by comma, but handle nested functions
      headers = []
      current_header = ''
      paren_count = 0
      
      for char in select_clause:
          if char == '(' and paren_count >= 0:
              paren_count += 1
              current_header += char
          elif char == ')' and paren_count > 0:
              paren_count -= 1
              current_header += char
          elif char == ',' and paren_count == 0:
              headers.append(current_header.strip())
              current_header = ''
          else:
              current_header += char
      
      # Add the last header
      if current_header:
          headers.append(current_header.strip())

      # Process each header to handle aliases
      processed_headers = []
      for header in headers:
          # Check for AS keyword
          if ' AS ' in header.upper():
              # Take the alias after AS
              alias = header.split(' AS ')[-1].strip()
              processed_headers.append(alias.strip('`" '))
          else:
              # If no AS, take the original column name
              processed_headers.append(header.strip('`" '))

      return processed_headers
          
