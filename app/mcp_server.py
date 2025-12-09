import sys
import os
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from fastmcp import FastMCP
from app.rag.rag_query_engine import rag_query
from app.rag.vectorstore import VectorStore 

mcp = FastMCP("cloudwalk-rag-mcp")

print("[SERVER] Loading Vector Store...")
try:

    vs = VectorStore(dim=768) 
    vs.load()
    print("[SERVER] Vector Store loaded successfully.")
except Exception as e:
    print(f"\n[CRITICAL WARNING] Could not load vector store: {e}")
    print("Queries will fail until 'data/vectorstore' is populated.\n")

@mcp.tool()
def cloudwalk_rag_query(question: str) -> dict:
    """
    Ask CloudWalk questions using Retrieval-Augmented Generation (RAG).
    """
    answer, sources = rag_query(question, vectorstore=vs)
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    mcp.run()