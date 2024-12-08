from typing import Any, Optional
import torch
import torch_directml

def get_device() -> torch.device:
    """Get the best available device (DirectML GPU or CPU)."""
    try:
        return torch_directml.device()
    except:
        return torch.device('cpu')

def move_to_device(data: Any, device: Optional[torch.device] = None) -> Any:
    """Move data to the specified device."""
    if device is None:
        device = get_device()
    
    if isinstance(data, torch.Tensor):
        return data.to(device)
    elif isinstance(data, dict):
        return {k: move_to_device(v, device) for k, v in data.items()}
    elif isinstance(data, list):
        return [move_to_device(item, device) for item in data]
    elif isinstance(data, tuple):
        return tuple(move_to_device(item, device) for item in data)
    return data

def optimize_memory():
    """Optimize GPU memory usage by clearing cache."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    # DirectML doesn't have explicit memory management functions
    # but we can force garbage collection
    import gc
    gc.collect()
