import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

from neo4j_client import Neo4jClient
from node_matcher import match_entities_to_nodes


def process_disruption_text(text, client, risk_level="high"):
    """
    Full pipeline: extract entities from text, match to Neo4j nodes,
    and update risk_level for any matched nodes if a disruption is detected.
    """
    result = match_entities_to_nodes(text, client)

    updated_nodes = []

    if result["has_disruption"] and result["matched_nodes"]:
        for node in result["matched_nodes"]:
            update_result = client.update_node_risk(node["name"], risk_level)
            if update_result:
                updated_nodes.append(update_result[0])
                print(f"⚠️  Risk updated: {node['name']} ({node['type']}) -> {risk_level}")
    else:
        print("No disruption detected or no matching nodes found. No updates made.")

    return {
        "disruption_keywords": result["disruption_keywords"],
        "matched_nodes": result["matched_nodes"],
        "updated_nodes": updated_nodes,
    }


if __name__ == "__main__":
    client = Neo4jClient()

    news_articles = [
        """A sudden port strike has broken out in Rotterdam, Netherlands, disrupting
        operations at one of Europe's busiest shipping hubs. Stuttgart Auto Factory
        in Germany, which relies on the port for exports, is expected to face
        significant delays.""",

        """Shenzhen Electronics Factory announced a temporary shutdown due to
        a fire at its main production facility in China.""",

        """Congo Cobalt Mines reported a shortage of skilled labor, causing
        delays in raw material shipments.""",

        """Port of Shanghai is experiencing significant congestion and delays
        following a recent earthquake near the coastal region.""",

        """Toyota City Plant in Japan halted operations temporarily following
        a workers protest over new labor policies.""",
    ]

    for text in news_articles:
        print(f"\n--- Processing article ---")
        process_disruption_text(text, client)

    client.close()
    