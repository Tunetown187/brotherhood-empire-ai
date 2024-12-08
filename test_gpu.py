import torch
import torch_directml

# Initialize the DML device
device = torch_directml.device()

print(f"DirectML device: {device}")

# Create a test tensor
x = torch.randn(100, 100, device=device)
y = torch.randn(100, 100, device=device)

# Perform a computation to test GPU acceleration
result = torch.matmul(x, y)

print("GPU computation successful!")
print(f"Result shape: {result.shape}")
