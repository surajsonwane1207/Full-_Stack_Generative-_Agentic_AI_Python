import os
import time
from celery import Celery
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Initialize Celery app
celery_app = Celery(
    "rag_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

DB_DIR = "./chroma_db"

@celery_app.task(bind=True)
def process_document(self, filename: str, content: str):
    """
    Background task to process a document, split it, embed it, 
    and store it in Chroma DB.
    """
    print(f"Worker received document: {filename}")
    
    # 1. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=content, metadata={"source": filename})]
    chunks = text_splitter.split_documents(docs)
    
    print(f"Worker split {filename} into {len(chunks)} chunks.")
    
    # Simulate processing time for large docs
    time.sleep(2)
    
    # 2. Embed & Store
    # Note: In a true production environment, you might want to use a shared 
    # remote vector DB (like Pinecone/Milvus) rather than local Chroma,
    # or ensure only one worker writes to Chroma at a time.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print(f"Worker finished processing: {filename}")
    return {"status": "success", "chunks_processed": len(chunks), "file": filename}
