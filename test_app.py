import os
import pytest
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

def test_document_loading():
    """Verify that the PDF manuals can be loaded correctly."""
    assert os.path.exists(DATA_DIR), "Data directory should exist."
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    assert len(documents) > 0, "Should load at least one document page."

    # Check if expected content is in the loaded documents
    content = " ".join([doc.page_content for doc in documents])
    assert "High Voltage Battery" in content or "Inverter" in content or "Hybrid Battery Pack" in content

def test_vectorstore_retrieval():
    """Verify that ChromaDB can retrieve relevant documents."""
    assert os.path.exists(CHROMA_DIR), "Chroma directory should exist."

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    # Simple query
    query = "battery error"
    retrieved_docs = db.similarity_search(query, k=2)

    assert len(retrieved_docs) > 0, "Should retrieve at least one document."
    assert "battery" in retrieved_docs[0].page_content.lower() or "voltage" in retrieved_docs[0].page_content.lower()
