import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

from fastapi import FastAPI, HTTPException
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


@app.get("/graph")
def get_graph():
    """
    Return the full graph in a format ready for React Flow:
    nodes with position/data, and edges with source/target/label.
    """
    client = Neo4jClient()

    node_query = """
    MATCH (n)
    WHERE n.name IS NOT NULL
    RETURN n.name AS name, labels(n)[0] AS type,
           coalesce(n.country, '-') AS country,
           coalesce(n.industry, '-') AS industry,
           coalesce(n.risk_level, 'low') AS risk_level,
           coalesce(n.predicted_risk_score, 0.0) AS predicted_risk_score
    """
    edge_query = """
    MATCH (a)-[r]->(b)
    WHERE a.name IS NOT NULL AND b.name IS NOT NULL
    RETURN a.name AS source, b.name AS target, type(r) AS relationship
    """

    raw_nodes = client.run_query(node_query)
    raw_edges = client.run_query(edge_query)
    client.close()

    nodes = [
        {
            "id": n["name"],
            "data": {
                "label": n["name"],
                "type": n["type"],
                "country": n["country"],
                "industry": n["industry"],
                "risk_level": n["risk_level"],
                "predicted_risk_score": n["predicted_risk_score"],
            },
        }
        for n in raw_nodes
    ]

    edges = [
        {
            "id": f"{e['source']}-{e['target']}",
            "source": e["source"],
            "target": e["target"],
            "label": e["relationship"],
        }
        for e in raw_edges
    ]

    return {"nodes": nodes, "edges": edges}


@app.get("/node/{node_name}")
def get_node_details(node_name: str):
    """Return full details for a single node by name."""
    client = Neo4jClient()

    query = """
    MATCH (n {name: $node_name})
    RETURN n.name AS name, labels(n)[0] AS type,
           coalesce(n.country, '-') AS country,
           coalesce(n.industry, '-') AS industry,
           coalesce(n.risk_level, 'low') AS risk_level,
           coalesce(n.predicted_risk_score, 0.0) AS predicted_risk_score
    """
    result = client.run_query(query, {"node_name": node_name})
    client.close()

    if not result:
        raise HTTPException(status_code=404, detail=f"Node '{node_name}' not found")

    return result[0]