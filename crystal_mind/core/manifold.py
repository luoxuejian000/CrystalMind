import torch
from typing import Callable, Dict, Optional

class Chart:
    def __init__(self, chart_id: int, phi: Callable, inv_phi: Callable, valid_region: Callable):
        self.chart_id = chart_id
        self.phi = phi
        self.inv_phi = inv_phi
        self.valid_region = valid_region

class Manifold:
    def __init__(self, name: str, dim: int, atlas: Dict[int, Chart], metric_fn: Callable):
        self.name = name
        self.dim = dim
        self.atlas = atlas
        self.metric_fn = metric_fn
        self.legal_region: Optional[Callable] = None

    def set_legal_region(self, region_fn: Callable):
        self.legal_region = region_fn

    def enforce_boundary(self, points: torch.Tensor) -> torch.Tensor:
        if self.legal_region is None:
            return points
        return self.legal_region(points)

def create_s1_manifold() -> Manifold:
    def phi0(theta): return theta % (2*torch.pi)
    def inv_phi0(x): return x
    def valid0(x): return (x > 0.01) & (x < 2*torch.pi - 0.01)
    chart0 = Chart(0, phi0, inv_phi0, valid0)
    def phi1(theta):
        theta_mod = theta % (2*torch.pi)
        return torch.where(theta_mod > torch.pi, theta_mod - 2*torch.pi, theta_mod)
    def inv_phi1(x): return x % (2*torch.pi)
    def valid1(x): return (x > -torch.pi + 0.01) & (x < torch.pi - 0.01)
    chart1 = Chart(1, phi1, inv_phi1, valid1)
    def metric_fn(coords):
        batch = coords.shape[0]
        return torch.eye(1).unsqueeze(0).expand(batch, -1, -1)
    m = Manifold("S1", 1, {0: chart0, 1: chart1}, metric_fn)
    m.set_legal_region(lambda x: torch.clamp(x, min=0.2, max=2.8))
    return m