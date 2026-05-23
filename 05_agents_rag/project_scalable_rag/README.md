# Project: Scalable RAG with Queues

This project demonstrates how to scale a Retrieval-Augmented Generation (RAG) system for production using FastAPI, Celery, and Redis.

## The Problem
Embedding large documents and inserting them into a Vector DB takes time. If you do this synchronously during an API request, the user's connection will time out.

## The Solution
1. **FastAPI**: Receives the document file via an HTTP POST request and immediately returns a `task_id`.
2. **Redis**: Acts as the message broker (queue) between the API and the worker.
3. **Celery Worker**: Picks up the task from Redis in the background, splits the text, generates embeddings via HuggingFace, and stores them in ChromaDB.

## Setup & Run

1. Start Redis:
   ```bash
   docker-compose up -d
   ```

2. Start the Celery Worker (in a new terminal):
   ```bash
   celery -A worker.celery_app worker --loglevel=info
   ```

3. Start the FastAPI server (in a new terminal):
   ```bash
   uvicorn main:app --reload
   ```

## Usage
Upload a text file to the API:
```bash
curl -X 'POST' \
  'http://localhost:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@../project_rag_pipeline/data/sample.txt'
```

Check the status of the task using the returned `task_id`:
```bash
curl http://localhost:8000/status/<YOUR_TASK_ID>
```
