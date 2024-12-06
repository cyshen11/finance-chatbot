"""Writer to generate SQL query"""

import os
from langchain import hub
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated
from typing_extensions import TypedDict
from components.utils import State
from langchain_community.utilities import SQLDatabase
import sqlite3

model = os.environ["model"]

def init_llm():
    """Initialize LLM"""
    llm = ChatOpenAI(model="gpt-4o-mini")
    return llm

class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]

def write_query(state: State):
    """Generate SQL query to fetch information.
    Args:
        state (State): Langgraph State
    """
    llm = init_llm()
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

    # Open database in read-only mode
    creator = lambda: sqlite3.connect('file:data/sqlite_db.db?mode=ro', uri=True)
    db = SQLDatabase.from_uri('sqlite:///' , engine_args={'creator': creator})

    # Update prompt
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}