from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(
    title="Ollama + FastAPI integration",
    description="A simple API wrapper for local Ollama models",
    version="1.0.0"
)

# Ollama default local URL
OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3" # Default model
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str

@app.get("/")
def root():
    return {"message": "Welcome to the Ollama FastAPI API. Use the /chat endpoint to generate text."}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ollama(request: ChatRequest):
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "stream": False,
        "options": {
            "temperature": request.temperature
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_URL, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            
            return ChatResponse(
                response=data.get("response", ""),
                model=data.get("model", request.model)
            )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error communicating with Ollama: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
