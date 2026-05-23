# Project: Local Ollama + FastAPI AI App

This project demonstrates how to build a RESTful API using FastAPI that wraps around a locally running large language model via Ollama.

## Prerequisites
1. **Ollama**: Must be installed and running on your system. 
   - Download from [ollama.com](https://ollama.com/)
   - Pull a model: `ollama run llama3` (or any other model you prefer)

## Setup

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```bash
   python main.py
   ```
   *Alternatively*: `uvicorn main:app --reload`

## Usage

The API runs on `http://localhost:8000`.

- **Swagger Documentation**: View the interactive API docs at `http://localhost:8000/docs`

**Sample cURL Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Why is the sky blue?",
  "model": "llama3",
  "temperature": 0.7
}'
```

## Architecture
- **FastAPI**: Provides robust, async routing and automatic OpenAPI documentation.
- **Pydantic**: Validates incoming JSON requests and formats responses.
- **HTTPX**: Used for async HTTP calls to the local Ollama daemon (`http://localhost:11434`).
