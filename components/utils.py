"""Utilities that define the RAG State class"""

from typing_extensions import TypedDict

class State(TypedDict):
    """RAG State

    Attrs:
        question (str): User question
        query (str): Generated query
        answer (str): Generated answer
        source (str): Document source link
    """
    question: str
    query: str
    answer: str
    source: str