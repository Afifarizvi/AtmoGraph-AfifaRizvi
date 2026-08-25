import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class RiskGNN(nn.Module):
    """
    A simple 2-layer Graph Convolutional Network that predicts a
    continuous risk score (0-1) for each node, based on its own
    features and its neighbors' features (i.e. ripple effect).
    """

    def __init__(self, in_channels, hidden_channels=16):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.output_layer = nn.Linear(hidden_channels, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        out = self.output_layer(x)
        out = torch.sigmoid(out)  # squash to 0-1 range (risk score)
        return out.squeeze(-1)


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.dirname(__file__))
    from graph_to_pyg import build_pyg_graph

    data, nodes, name_to_idx = build_pyg_graph()

    model = RiskGNN(in_channels=data.num_node_features)

    print("=== Model Architecture ===")
    print(model)

    # Forward pass test (untrained, just checking shapes work)
    with torch.no_grad():
        predictions = model(data.x, data.edge_index)

    print(f"\n=== Forward Pass Output ===")
    print(f"Output shape: {predictions.shape} (should match number of nodes: {data.num_nodes})")

    print("\n=== Sample Predictions (untrained, random weights) ===")
    for node in nodes[:5]:
        idx = name_to_idx[node["name"]]
        print(f"{node['name']:35s} -> predicted risk: {predictions[idx].item():.4f}")