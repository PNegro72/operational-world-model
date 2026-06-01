"""Static registries for tools and prompt modules."""

from .prompt_registry import PROMPT_MODULE_REGISTRY
from .tool_registry import TOOL_REGISTRY

__all__ = ["PROMPT_MODULE_REGISTRY", "TOOL_REGISTRY"]
