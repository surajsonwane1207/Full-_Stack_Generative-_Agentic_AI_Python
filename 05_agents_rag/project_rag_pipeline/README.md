# Project: Document RAG Pipeline with LangChain

This project demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline running 100% locally.

## Components
1. **Document Loading**: Reads text files from the `data/` directory.
2. **Text Splitting**: Chunks text into smaller, overlapping segments.
3. **Embeddings**: Uses `sentence-transformers` (all-MiniLM-L6-v2) to convert chunks to vectors.
4. **Vector Store**: Uses Chroma DB to store and query the embeddings.
5. **LLM**: Uses local Ollama (`llama3` model) to generate the final answer based on the retrieved context.

## Prerequisites
- Ollama installed and running.
- Llama3 pulled (`ollama run llama3`).

## Setup & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your documents:
   Place any `.txt` files inside the `data/` directory. (A sample file is already provided).

3. Run the pipeline:
   ```bash
   python rag.py
   ```

## How it works
When you ask a question, the system embeds your question, searches Chroma DB for the most similar text chunks, and then passes those chunks alongside your question to Ollama. The LLM synthesizes an answer using *only* the provided context.
