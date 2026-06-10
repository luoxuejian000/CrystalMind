import torch
from typing import Callable, Optional

class FiberBundle:
    def __init__(self, name: str, base: 'Manifold', fiber_dim: int, allowed_subset: Optional[Callable] = None):
        self.name = name
        self.base = base
        self.fiber_dim = fiber_dim
        self.allowed_subset = allowed_subset

    def project(self, fiber_element: 'FiberElement') -> torch.Tensor:
        return fiber_element.point.coords

    def check_fiber_valid(self, fiber_coords: torch.Tensor) -> bool:
        if self.allowed_subset is None:
            return True
        return self.allowed_subset(fiber_coords).all().item()

class FiberElement:
    def __init__(self, bundle: FiberBundle, point: torch.Tensor, fiber_coords: torch.Tensor):
        self.bundle = bundle
        self.point = point
        self.fiber_coords = fiber_coords