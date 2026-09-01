import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

from fastapi import FastAPI
from neo4j_client import Neo4jClient

app = FastAPI(title="AtmoGraph API", description="Supply Chain Ripple Effect Predictor Backend")


@app.get("/")
def root():
    return {"message": "AtmoGraph API is running", "status": "ok"}


@app.get("/health")
def health_check():
    """Verify the API and Neo4j connection are both working."""
    try:
        client = Neo4jClient()
        node_counts = client.get_node_counts()
        client.close()
        return {"api": "ok", "neo4j": "connected", "node_counts": node_counts}
    except Exception as e:
        return {"api": "ok", "neo4j": "error", "detail": str(e)}