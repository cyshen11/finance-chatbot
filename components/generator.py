"""Generator to generate response based on corresponding SQL query"""
from langchain_openai import ChatOpenAI
from components.utils import State

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}