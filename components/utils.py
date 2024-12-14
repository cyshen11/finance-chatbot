"""Utilities that define the RAG State class"""

from typing_extensions import List, TypedDict
from langchain_core.documents import Document

class State(TypedDict):
    """RAG State

    Attrs:
        question (str): User question
        context (list(Document)): Retrieved list of documents from ChromaDB
        answer (str): Generated answer
        source (str): Document source link
    """
    question: str
    context: List[Document]
    answer: str
    source: str