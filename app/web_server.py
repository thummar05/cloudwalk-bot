
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os

from app.rag.rag_query_engine import rag_query
from app.rag.vectorstore import VectorStore

app = FastAPI()

print("[WEB] Loading Vector Store...")
try:

    vs = VectorStore(dim=768)
    vs.load()
    print("[WEB] Vector Store loaded.")
except Exception as e:
    print(f"[ERROR] Failed to load Vector Store: {e}")
    vs = None

class QueryRequest(BaseModel):
    question: str


@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    if not vs:
        raise HTTPException(status_code=500, detail="Vector Store not initialized")
    

    answer, sources = rag_query(request.question, vectorstore=vs)
    
    return {
        "answer": answer,
        "sources": sources
    }


ui_path = os.path.join(os.getcwd(), "ui")
if os.path.exists(ui_path):
    app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
else:
    print(f"[WARNING] UI folder not found at {ui_path}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)