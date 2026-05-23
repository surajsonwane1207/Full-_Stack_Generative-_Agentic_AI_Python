import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Setup Data Directory
DATA_DIR = "./data"
DB_DIR = "./chroma_db"

def build_rag_pipeline():
    print("1. Loading documents...")
    # Load all text files in the data directory
    loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    print("2. Splitting text...")
    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    print("3. Initializing Embedding Model...")
    # Use HuggingFace's all-MiniLM-L6-v2 for local, fast embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("4. Creating Vector Database...")
    # Store chunks and embeddings in Chroma DB
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    print("5. Initializing Local LLM (Ollama)...")
    # Make sure you have Ollama running locally with the llama3 model
    llm = Ollama(model="llama3")

    print("6. Creating Chain...")
    # Define the prompt template
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context:
    {context}

    Question: {question}

    Answer:"""
    prompt = PromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Build the LCEL (LangChain Expression Language) pipeline
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: {DATA_DIR} does not exist. Please create it and add text files.")
        exit(1)
        
    print("--- Initializing Local RAG Pipeline ---")
    chain = build_rag_pipeline()
    print("--- Pipeline Ready ---\n")
    
    # Test Query
    question = "What does the bootcamp teach?"
    print(f"Question: {question}")
    print("Thinking...")
    
    response = chain.invoke(question)
    
    print("\nAnswer:")
    print(response)
