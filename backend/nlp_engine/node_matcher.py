import sys
import os

# Allow importing from backend/graph_db
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

from neo4j_client import Neo4jClient
from entity_extractor import extract_entities


def get_all_graph_node_names(client):
    """Fetch all node names from Neo4j, grouped with their label/type."""
    query = """
    MATCH (n)
    WHERE n.name IS NOT NULL
    RETURN n.name AS name, labels(n)[0] AS type
    """
    results = client.run_query(query)
    return {row["name"]: row["type"] for row in results}


def match_entities_to_nodes(text, client):
    """
    Extract entities from text and match them against known Neo4j node names.
    Returns a list of matched nodes with their type, plus disruption info.
    """
    extraction = extract_entities(text)
    all_nodes = get_all_graph_node_names(client)

    matched_nodes = []

    # Try direct match first (exact name match)
    for org in extraction["organizations"]:
        if org in all_nodes:
            matched_nodes.append({"name": org, "type": all_nodes[org], "match_type": "exact"})

    # Try partial/substring match as a fallback (handles cases NER might miss or shorten)
    text_lower = text.lower()
    for node_name, node_type in all_nodes.items():
        if node_name.lower() in text_lower and node_name not in [m["name"] for m in matched_nodes]:
            matched_nodes.append({"name": node_name, "type": node_type, "match_type": "substring"})

    return {
        "matched_nodes": matched_nodes,
        "locations": extraction["locations"],
        "disruption_keywords": extraction["disruption_keywords"],
        "has_disruption": extraction["has_disruption"],
    }


if __name__ == "__main__":
    client = Neo4jClient()

    sample_texts = [
        """A sudden port strike has broken out in Rotterdam, Netherlands,
        disrupting operations. Stuttgart Auto Factory in Germany is expected
        to face significant delays.""",

        """Congo Cobalt Mines reported a shortage of skilled labor, causing
        delays in raw material shipments to Shenzhen Electronics Factory.""",
    ]

    for i, text in enumerate(sample_texts, 1):
        print(f"\n=== Sample {i} ===")
        result = match_entities_to_nodes(text, client)
        print(result)

    client.close()