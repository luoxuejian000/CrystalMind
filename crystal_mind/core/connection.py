import torch
from typing import Dict, Optional

class Connection:
    def __init__(self, bundle: 'FiberBundle', local_forms: Optional[Dict[int, torch.Tensor]] = None):
        self.bundle = bundle
        self.local_forms = local_forms or {}

    def parallel_transport(self, curve: torch.Tensor, initial_fiber: torch.Tensor) -> torch.Tensor:
        steps = curve.shape[0]
        fibers = [initial_fiber]
        f = initial_fiber.clone()
        for i in range(steps - 1):
            f = f
            fibers.append(f)
        return torch.stack(fibers, dim=0)