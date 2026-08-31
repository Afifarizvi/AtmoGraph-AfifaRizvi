import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

import torch
from graph_to_pyg import build_pyg_graph
from model import RiskGNN
from neo4j_client import Neo4jClient


def run_inference_and_update_graph():
    # Rebuild the graph (fresh data + structure from Neo4j)
    data, nodes, name_to_idx = build_pyg_graph()

    # Load the trained model
    model = RiskGNN(in_channels=data.num_node_features)
    model_path = os.path.join(os.path.dirname(__file__), "risk_gnn_weights.pt")
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # Run predictions on the full graph
    with torch.no_grad():
        predictions = model(data.x, data.edge_index)

    # Write predictions back to Neo4j
    client = Neo4jClient()
    idx_to_name = {v: k for k, v in name_to_idx.items()}

    print("=== Writing predictions to Neo4j ===")
    for i in range(data.num_nodes):
        name = idx_to_name[i]
        score = round(predictions[i].item(), 4)
        client.update_predicted_risk(name, score)
        print(f"{name:35s} -> predicted_risk_score: {score}")

    client.close()
    print("\n✅ All predictions written to Neo4j as 'predicted_risk_score' property")


if __name__ == "__main__":
    run_inference_and_update_graph()