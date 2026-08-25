import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "graph_db"))

import torch
from torch_geometric.data import Data
from neo4j_client import Neo4jClient

# Encoding maps
NODE_TYPES = ["Supplier", "Manufacturer", "Port", "Retailer"]
INDUSTRIES = ["Electronics", "Automotive", "Pharmaceuticals", "-"]
RISK_LEVELS = {"low": 0.0, "medium": 0.5, "high": 1.0}


def fetch_all_nodes(client):
    query = """
    MATCH (n)
    WHERE n.name IS NOT NULL
    RETURN n.name AS name, labels(n)[0] AS type,
           coalesce(n.industry, '-') AS industry,
           coalesce(n.risk_level, 'low') AS risk_level
    """
    return client.run_query(query)


def fetch_all_edges(client):
    query = """
    MATCH (a)-[r]->(b)
    WHERE a.name IS NOT NULL AND b.name IS NOT NULL
    RETURN a.name AS source, b.name AS target, type(r) AS rel_type
    """
    return client.run_query(query)


def one_hot(value, categories):
    vec = [0.0] * len(categories)
    if value in categories:
        vec[categories.index(value)] = 1.0
    return vec


def build_node_features(node):
    type_vec = one_hot(node["type"], NODE_TYPES)
    industry_vec = one_hot(node["industry"], INDUSTRIES)
    risk_val = [RISK_LEVELS.get(node["risk_level"], 0.0)]
    return type_vec + industry_vec + risk_val


def build_pyg_graph():
    client = Neo4jClient()

    nodes = fetch_all_nodes(client)
    edges = fetch_all_edges(client)

    client.close()

    # Map node name -> index
    name_to_idx = {node["name"]: i for i, node in enumerate(nodes)}

    # Build feature matrix
    features = [build_node_features(node) for node in nodes]
    x = torch.tensor(features, dtype=torch.float)

    # Build edge_index
    edge_list = []
    for edge in edges:
        src_idx = name_to_idx.get(edge["source"])
        tgt_idx = name_to_idx.get(edge["target"])
        if src_idx is not None and tgt_idx is not None:
            edge_list.append([src_idx, tgt_idx])

    edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()

    data = Data(x=x, edge_index=edge_index)

    return data, nodes, name_to_idx


if __name__ == "__main__":
    data, nodes, name_to_idx = build_pyg_graph()

    print("=== PyG Graph Summary ===")
    print(data)
    print(f"\nNumber of nodes: {data.num_nodes}")
    print(f"Number of edges: {data.num_edges}")
    print(f"Feature vector size per node: {data.num_node_features}")

    print("\n=== Sample Node Features (first 3 nodes) ===")
    for node in nodes[:3]:
        idx = name_to_idx[node["name"]]
        print(f"{node['name']:35s} -> {data.x[idx].tolist()}")