"""Utilities that define the RAG State class"""

from typing_extensions import TypedDict

class State(TypedDict):
    """RAG State

    Attrs:
        question (str): User question
        query (str): Generated query
        result (str): Query result
        answer (str): Generated answer
    """
    question: str
    query: str
    result: str
    answer: str