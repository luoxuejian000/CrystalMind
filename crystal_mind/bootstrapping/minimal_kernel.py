import torch, logging
from crystal_mind.core.manifold import create_s1_manifold
from crystal_mind.core.fiber_bundle import FiberBundle, FiberElement
from crystal_mind.core.connection import Connection
from crystal_mind.core.category_checker import CategoryChecker
from crystal_mind.core.snapshot import StateSnapshot

logger = logging.getLogger(__name__)

class MinimalKernel:
    def __init__(self):
        self.manifold = create_s1_manifold()
        self.obs_bundle = FiberBundle("observation", self.manifold, 1)
        self.act_bundle = FiberBundle("action", self.manifold, 1, allowed_subset=lambda x: (x>=-0.5)&(x<=0.5))
        self.connection = Connection(self.obs_bundle)
        self.checker = CategoryChecker()
        self._verify()

    def _verify(self):
        logger.info("Bootstrapping minimal kernel...")
        charts = list(self.manifold.atlas.values())
        self.checker.assert_chart_transition_inverse(charts[0], charts[1])
        logger.info("Minimal kernel verified.")

    def get_snapshot(self, angle: float, fiber_val: float) -> StateSnapshot:
        coords = torch.tensor([[angle]])
        chart_id = 0 if (0.01<angle<torch.pi-0.01) or (torch.pi+0.01<angle<2*torch.pi-0.01) else 1
        margin = min(angle-0.2, 2.8-angle)
        return StateSnapshot(
            manifold_name="S1", coordinates=[angle], chart_id=chart_id,
            fiber_values={'obs':[fiber_val]},
            constraint_margins={'angular_margin':margin},
            harmonic_score=0.85, unified_score=0.82, developmental_score=0.74,
            adversarial_score=0.12, is_safe=margin>0.05
        )