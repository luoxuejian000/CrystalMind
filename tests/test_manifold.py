import torch
from crystal_mind.core.manifold import create_s1_manifold

def test_manifold():
    m = create_s1_manifold()
    assert m.name == "S1"
    pts = torch.tensor([0.0,3.0])
    clamped = m.enforce_boundary(pts)
    assert (clamped >= 0.2).all() and (clamped <= 2.8).all()