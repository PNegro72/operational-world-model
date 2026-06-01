"""Operational world model implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .prompt_builder import DynamicPromptBuilder
from .routers import ControlRouter, PromptModuleRouter, SkillRouter, ToolRouter
from .schemas import OperationalConfiguration, OperationalState, OperationalTrace


class BaseOperationalWorldModel(ABC):
    """Base interface for operational world models."""

    @abstractmethod
    def predict(
        self,
        state: OperationalState,
        configuration: OperationalConfiguration,
    ) -> OperationalTrace:
        """Predict the next operational trace for a state."""


class RuleBasedOperationalWorldModel(BaseOperationalWorldModel):
    """Deterministic dependency-free model using simple routers."""

    def __init__(
        self,
        control_router: ControlRouter | None = None,
        skill_router: SkillRouter | None = None,
        prompt_module_router: PromptModuleRouter | None = None,
        tool_router: ToolRouter | None = None,
        prompt_builder: DynamicPromptBuilder | None = None,
    ) -> None:
        self.control_router = control_router or ControlRouter()
        self.skill_router = skill_router or SkillRouter()
        self.prompt_module_router = prompt_module_router or PromptModuleRouter()
        self.tool_router = tool_router or ToolRouter()
        self.prompt_builder = prompt_builder or DynamicPromptBuilder()

    def predict(
        self,
        state: OperationalState,
        configuration: OperationalConfiguration,
    ) -> OperationalTrace:
        control_decision = self.control_router.route(state, configuration)
        skill_decision = self.skill_router.route(state, control_decision)
        selected_prompt_modules = self.prompt_module_router.route(
            state,
            configuration,
            control_decision,
            skill_decision,
        )
        selected_tools = self.tool_router.route(state, configuration, skill_decision)
        prompt = self.prompt_builder.build(
            state,
            control_decision,
            skill_decision,
            selected_prompt_modules,
        )
        predicted_state, notes = self._predict_state(
            state,
            control_decision.action,
            skill_decision.skill_name,
            skill_decision.inputs,
        )

        return OperationalTrace(
            state=state,
            configuration=configuration,
            control_decision=control_decision,
            skill_decision=skill_decision,
            selected_prompt_modules=selected_prompt_modules,
            selected_tools=selected_tools,
            prompt=prompt,
            predicted_state=predicted_state,
            notes=notes,
        )

    def _predict_state(
        self,
        state: OperationalState,
        control_action: str,
        skill_name: str,
        skill_inputs: dict[str, Any],
    ) -> tuple[OperationalState, list[str]]:
        facts = dict(state.facts)
        notes: list[str] = []

        if skill_name == "wallet_reconciliation":
            delta = float(skill_inputs.get("balance_delta", 0))
            facts["reconciliation_delta"] = delta
            facts["reconciliation_status"] = "matched" if delta == 0 else "requires_adjustment"
            notes.append("Wallet reconciliation rule evaluated balance delta.")

        if skill_name == "sql_skill":
            facts["control"] = skill_inputs.get("control", facts.get("parent_control"))
            facts["suggested_subcontrol"] = skill_inputs.get("suggested_subcontrol", "core_vs_site")
            facts["group_by"] = skill_inputs.get("group_by", "fecha")
            facts["metric"] = skill_inputs.get("metric", "incosistencias")
            facts["query_intent"] = "data_query"
            facts["analysis_mode"] = "grouped_count_by_date"
            facts["requires_sql"] = True
            notes.append("SQL planning rule selected control, subcontrol, grouping, and metric.")

        if control_action == "escalate":
            facts["escalation_required"] = True
            notes.append("Escalation flag added to predicted state.")

        return replace(state, facts=facts), notes
