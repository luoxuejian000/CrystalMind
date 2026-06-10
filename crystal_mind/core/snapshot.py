from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class StateSnapshot:
    manifold_name: str
    coordinates: List[float]
    chart_id: int
    fiber_values: Dict[str, List[float]]
    constraint_margins: Dict[str, float]
    harmonic_score: float
    unified_score: float
    developmental_score: float
    adversarial_score: float
    is_safe: bool
    dH_dt: float = 0.0
    d2H_dt2: float = 0.0
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)