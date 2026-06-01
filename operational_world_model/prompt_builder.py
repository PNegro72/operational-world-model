"""Dynamic prompt construction without external LLM integration."""

from __future__ import annotations

from .schemas import ControlDecision, OperationalState, SkillDecision


class DynamicPromptBuilder:
    """Builds a deterministic prompt from routed modules."""

    def build(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
        skill_decision: SkillDecision,
        modules: list[str],
    ) -> str:
        sections: list[str] = []

        for module in modules:
            if module == "summary":
                sections.append(self._summary(state, control_decision, skill_decision))
            elif module == "open_items":
                sections.append(self._open_items(state))
            elif module == "risk":
                sections.append(self._risk(state, control_decision))
            elif module == "reconciliation":
                sections.append(self._reconciliation(skill_decision))
            elif module == "pf_context":
                sections.append(self._pf_context(state))
            elif module == "agentic_wh_rules":
                sections.append("Agentic WH: plan control, skill, prompt modules, and tools without executing them.")
            elif module == "control_routing_rules":
                sections.append("Control routing: map Conciliaciones: Interfaces to core_vs_site for Plazo Fijo.")
            elif module == "sql_generation_rules":
                sections.append("SQL generation: answer date-based inconsistency questions with grouped counts by fecha.")
            elif module == "core_vs_site_rules":
                sections.append("Core vs Site: analyze records from Core toward Site/interface. Do not generate inverse analysis unless explicitly requested and supported.")
            else:
                sections.append(f"{module.title()}: enabled")

        return "\n\n".join(section for section in sections if section)

    def _summary(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
        skill_decision: SkillDecision,
    ) -> str:
        return (
            f"Operational state {state.state_id} in domain {state.domain}.\n"
            f"Control action: {control_decision.action} "
            f"(priority {control_decision.priority}).\n"
            f"Skill: {skill_decision.skill_name} "
            f"(confidence {skill_decision.confidence:.2f})."
        )

    def _open_items(self, state: OperationalState) -> str:
        if not state.open_items:
            return ""
        items = "\n".join(f"- {item}" for item in state.open_items)
        return f"Open items:\n{items}"

    def _risk(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
    ) -> str:
        constraints = ", ".join(control_decision.constraints) or "none"
        return f"Risk level: {state.risk_level}. Constraints: {constraints}."

    def _reconciliation(self, skill_decision: SkillDecision) -> str:
        delta = skill_decision.inputs.get("balance_delta", 0)
        return f"Reconciliation delta: {delta}. Verify source balances before action."

    def _pf_context(self, state: OperationalState) -> str:
        question = state.facts.get("question", "")
        product = state.facts.get("product", "")
        origin = state.facts.get("control_origin", "")
        return f"PF context: product={product}; control_origin={origin}; question={question}"
