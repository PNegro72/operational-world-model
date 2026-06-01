"""Dynamic prompt assembly without owning prompt content."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Mapping

from .registries.prompt_registry import PROMPT_MODULE_REGISTRY, PromptModuleDefinition
from .schemas import ControlDecision, OperationalState, SkillDecision


class DynamicPromptBuilder:
    """Loads markdown prompt modules and interpolates operational variables."""

    _VARIABLE_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")

    def __init__(
        self,
        prompt_registry: Mapping[str, PromptModuleDefinition] | None = None,
        base_path: Path | None = None,
    ) -> None:
        self.prompt_registry = prompt_registry or PROMPT_MODULE_REGISTRY
        self.base_path = base_path or Path(__file__).resolve().parents[1]

    def build(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
        skill_decision: SkillDecision,
        modules: list[str],
        selected_tools: list[str] | None = None,
    ) -> str:
        context = self._build_context(
            state,
            control_decision,
            skill_decision,
            selected_tools or [],
        )
        sections = [self._load_module(module, context) for module in modules]
        return "\n\n".join(section for section in sections if section)

    def _load_module(self, module_name: str, context: Mapping[str, object]) -> str:
        if module_name not in self.prompt_registry:
            known_modules = ", ".join(sorted(self.prompt_registry))
            raise ValueError(f"Unknown prompt module '{module_name}'. Known modules: {known_modules}")

        module = self.prompt_registry[module_name]
        path = self._resolve_path(module["path"])
        if not path.exists():
            raise FileNotFoundError(
                f"Prompt module '{module_name}' file does not exist: {path}"
            )

        content = path.read_text(encoding="utf-8")
        return self._interpolate(content, context).strip()

    def _resolve_path(self, path_value: str) -> Path:
        path = Path(path_value)
        if path.is_absolute():
            return path
        return self.base_path / path

    def _interpolate(self, content: str, context: Mapping[str, object]) -> str:
        def replace(match: re.Match[str]) -> str:
            variable_name = match.group(1)
            value = context.get(variable_name, "")
            return str(value) if value is not None else ""

        return self._VARIABLE_PATTERN.sub(replace, content)

    def _build_context(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
        skill_decision: SkillDecision,
        selected_tools: list[str],
    ) -> dict[str, object]:
        context: dict[str, object] = dict(state.facts)
        context.update(skill_decision.inputs)
        context.update(
            {
                "domain": state.domain,
                "state_id": state.state_id,
                "control_action": control_decision.action,
                "control_priority": control_decision.priority,
                "control_rationale": control_decision.rationale,
                "control_constraints": ", ".join(control_decision.constraints),
                "skill_name": skill_decision.skill_name,
                "skill_confidence": f"{skill_decision.confidence:.2f}",
                "skill_rationale": skill_decision.rationale,
                "selected_tools": ", ".join(selected_tools),
                "signals": ", ".join(state.signals),
                "risk_level": state.risk_level,
                "open_items": "\n".join(f"- {item}" for item in state.open_items),
            }
        )
        return context
