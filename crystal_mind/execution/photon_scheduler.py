from typing import Any, List
from .tool_catalog import ToolCatalog, ToolStatus
import logging

logger = logging.getLogger(__name__)

class PhotonScheduler:
    def __init__(self, catalog: ToolCatalog):
        self.catalog = catalog
        self.history: List[dict] = []

    def execute_tool(self, tool_name: str, input_data: Any, context: dict = None) -> Any:
        rec = self.catalog.get(tool_name)
        if not rec: raise ValueError(f"Tool {tool_name} not found")
        if rec.status != ToolStatus.APPROVED: raise PermissionError(f"Tool {tool_name} not approved")
        res = rec.function(input_data)
        self.history.append({'tool':tool_name,'input':input_data,'output':res,'context':context})
        return res