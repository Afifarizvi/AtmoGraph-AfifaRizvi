import sys
import os

sys.path.append(os.path.dirname(__file__))

import torch
import torch.nn.functional as F
from graph_to_pyg import build_pyg_graph
from model import RiskGNN


def train():
    data, nodes, name_to_idx = build_pyg_graph()

    model = RiskGNN(in_channels=data.num_node_features)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    print("=== Training RiskGNN ===")
    model.train()
    for epoch in range(1, 201):
        optimizer.zero_grad()
        predictions = model(data.x, data.edge_index)
        loss = F.mse_loss(predictions, data.y)
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0 or epoch == 1:
            print(f"Epoch {epoch:3d} | Loss: {loss.item():.4f}")

    print("\n=== Final Predictions vs Actual (all nodes) ===")
    model.eval()
    with torch.no_grad():
        final_predictions = model(data.x, data.edge_index)

    for node in nodes:
        idx = name_to_idx[node["name"]]
        print(f"{node['name']:35s} | actual: {data.y[idx].item():.2f} | predicted: {final_predictions[idx].item():.4f}")

    return model, data, nodes, name_to_idx


if __name__ == "__main__":
    train()