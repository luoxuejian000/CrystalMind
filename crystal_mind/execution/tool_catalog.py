from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional
from enum import Enum

class ToolStatus(Enum):
    REGISTERED = "registered"
    TESTED = "tested"
    APPROVED = "approved"
    DEPRECATED = "deprecated"

@dataclass
class ToolRecord:
    name: str
    version: str
    function: Callable
    input_type: str
    output_type: str
    preconditions: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    status: ToolStatus = ToolStatus.REGISTERED
    approval_required: bool = True

class ToolCatalog:
    def __init__(self):
        self._tools: Dict[str, ToolRecord] = {}
    def add(self, record: ToolRecord): self._tools[record.name] = record
    def get(self, name: str) -> Optional[ToolRecord]: return self._tools.get(name)
    def list_by_status(self, status: ToolStatus): return [t for t in self._tools.values() if t.status==status]
    def approve(self, name: str):
        if name in self._tools: self._tools[name].status = ToolStatus.APPROVED
    def deprecate(self, name: str):
        if name in self._tools: self._tools[name].status = ToolStatus.DEPRECATED