import os
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import Annotated
from typing_extensions import TypedDict
from utils import State
from langchain_community.utilities import SQLDatabase

model = os.environ["model"]

def init_llm():
    """Initialize LLM"""

    if model == "Google Gemini 1.5 Flash-8B":
      llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b")
    elif model == "OpenAI gpt-4o-mini":
      llm = ChatOpenAI(model="gpt-4o-mini")

    return llm

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
    """Generate SQL query to fetch information."""
    llm = init_llm()
    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
    db = SQLDatabase.from_uri("file:data/sqlite_db.db?mode=ro")

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