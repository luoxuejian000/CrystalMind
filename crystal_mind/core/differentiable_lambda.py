import torch
from typing import Callable

class DifferentiableLambda:
    @staticmethod
    def compose(f: Callable, g: Callable) -> Callable:
        return lambda x: f(g(x))

    @staticmethod
    def differentiate(f: Callable, x: torch.Tensor) -> torch.Tensor:
        x = x.detach().clone().requires_grad_(True)
        y = f(x)
        return torch.autograd.grad(y, x, create_graph=True)[0]

    @staticmethod
    def optimize(cost_fn: Callable, init: torch.Tensor, steps=100, lr=0.01) -> torch.Tensor:
        x = init.clone().detach().requires_grad_(True)
        optim = torch.optim.SGD([x], lr=lr)
        for _ in range(steps):
            optim.zero_grad()
            loss = cost_fn(x)
            loss.backward()
            optim.step()
        return x.detach()