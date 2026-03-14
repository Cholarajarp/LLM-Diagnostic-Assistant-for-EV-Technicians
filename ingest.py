import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

def ingest_data():
    print(f"Loading PDFs from {DATA_DIR}...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    print(f"Loaded {len(documents)} document pages.")

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Creating Chroma vector store at {CHROMA_DIR}...")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
    print("Ingestion complete. Data persisted to local ChromaDB.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found. Please run generate_manuals.py first.")
    else:
        ingest_data()
