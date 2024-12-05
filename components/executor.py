from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from components.utils import State
from langchain_community.utilities import SQLDatabase
import sqlite3

def execute_query(state: State):
    """Execute SQL query."""
    creator = lambda: sqlite3.connect('file:data/sqlite_db.db?mode=ro', uri=True)
    db = SQLDatabase.from_uri('sqlite:///' , engine_args={'creator': creator})

    execute_query_tool = QuerySQLDataBaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}