from typing import Dict, Any, Callable, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MessageType(Enum):
    ASK="ask"; CONFIRM="confirm"; GEN="gen"; EXEC="exec"; APPROVE="approve"; REJECT="reject"; NOTIFY="notify"

class Hub:
    def __init__(self):
        self.endpoints: Dict[str, Callable] = {}
        self.log: List[dict] = []

    def register(self, name: str, handler: Callable):
        self.endpoints[name] = handler

    async def send(self, msg: dict) -> Any:
        target = msg.get('to')
        if not target: raise ValueError("Missing 'to'")
        handler = self.endpoints.get(target)
        if not handler: raise ValueError(f"Unknown endpoint {target}")
        self.log.append(msg)
        return await handler(msg)