from fastapi import FastAPI, File, UploadForm, UploadFile, BackgroundTasks
from pydantic import BaseModel
from worker import process_document
import os

app = FastAPI(title="Scalable RAG API")

class TaskResponse(BaseModel):
    task_id: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Scalable RAG API."}

@app.post("/upload", response_model=TaskResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a document. It reads the file and immediately 
    offloads the heavy embedding work to a Celery background worker.
    """
    content = await file.read()
    text_content = content.decode("utf-8")
    
    # Dispatch task to Celery queue
    task = process_document.delay(file.filename, text_content)
    
    return TaskResponse(
        task_id=task.id,
        message=f"Document '{file.filename}' queued for processing."
    )

@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    from worker import celery_app
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
