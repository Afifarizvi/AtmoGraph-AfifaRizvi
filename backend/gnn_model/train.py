import sys
import os
import random

sys.path.append(os.path.dirname(__file__))

import torch
import torch.nn.functional as F
from graph_to_pyg import build_pyg_graph
from model import RiskGNN


def create_train_test_masks(data, nodes, test_ratio=0.25, seed=42):
    """
    Split nodes into train/test sets, keeping the split balanced
    across high-risk and low-risk nodes so the test set isn't trivial.
    """
    random.seed(seed)
    num_nodes = data.num_nodes

    high_risk_idx = [i for i in range(num_nodes) if data.y[i].item() > 0]
    low_risk_idx = [i for i in range(num_nodes) if data.y[i].item() == 0]

    random.shuffle(high_risk_idx)
    random.shuffle(low_risk_idx)

    n_test_high = max(1, int(len(high_risk_idx) * test_ratio))
    n_test_low = max(1, int(len(low_risk_idx) * test_ratio))

    test_idx = set(high_risk_idx[:n_test_high] + low_risk_idx[:n_test_low])
    train_idx = set(range(num_nodes)) - test_idx

    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    for i in train_idx:
        train_mask[i] = True
    for i in test_idx:
        test_mask[i] = True

    return train_mask, test_mask


def train():
    data, nodes, name_to_idx = build_pyg_graph()
    train_mask, test_mask = create_train_test_masks(data, nodes)

    print(f"Train nodes: {train_mask.sum().item()} | Test nodes: {test_mask.sum().item()}")

    model = RiskGNN(in_channels=data.num_node_features)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    print("\n=== Training RiskGNN (train nodes only) ===")
    model.train()
    for epoch in range(1, 301):
        optimizer.zero_grad()
        predictions = model(data.x, data.edge_index)

        # Only compute loss on training nodes
        loss = F.mse_loss(predictions[train_mask], data.y[train_mask])
        loss.backward()
        optimizer.step()

        if epoch % 30 == 0 or epoch == 1:
            model.eval()
            with torch.no_grad():
                test_preds = model(data.x, data.edge_index)
                test_loss = F.mse_loss(test_preds[test_mask], data.y[test_mask])
            model.train()
            print(f"Epoch {epoch:3d} | Train Loss: {loss.item():.4f} | Test Loss: {test_loss.item():.4f}")

    print("\n=== Test Set Evaluation (nodes NOT seen during loss calculation) ===")
    model.eval()
    with torch.no_grad():
        final_predictions = model(data.x, data.edge_index)

    idx_to_name = {v: k for k, v in name_to_idx.items()}
    for i in range(data.num_nodes):
        if test_mask[i]:
            name = idx_to_name[i]
            print(f"{name:35s} | actual: {data.y[i].item():.2f} | predicted: {final_predictions[i].item():.4f}")

    return model, data, nodes, name_to_idx


if __name__ == "__main__":
    train()