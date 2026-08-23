import torch
import torch_geometric

print("=== Environment Check ===")
print(f"PyTorch version: {torch.__version__}")
print(f"PyTorch Geometric version: {torch_geometric.__version__}")
print(f"MPS (Apple Silicon GPU) available: {torch.backends.mps.is_available()}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Quick sanity test: create a tiny graph and run a basic GCN layer
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

# 3 nodes, 2 features each
x = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=torch.float)

# Edges: 0->1, 1->2 (edge_index format required by PyG)
edge_index = torch.tensor([[0, 1], [1, 2]], dtype=torch.long).t().contiguous()

data = Data(x=x, edge_index=edge_index)

print("\n=== Tiny Test Graph ===")
print(data)

conv = GCNConv(in_channels=2, out_channels=4)
output = conv(data.x, data.edge_index)

print("\n=== GCN Layer Output ===")
print(output)
print("\n PyTorch Geometric is working correctly!")