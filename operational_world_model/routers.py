"""Small rule-based routers for operational decisions."""

from __future__ import annotations

from .schemas import ControlDecision, OperationalConfiguration, OperationalState, SkillDecision


class ControlRouter:
    """Selects the next control action from state signals and risk."""

    def route(
        self,
        state: OperationalState,
        configuration: OperationalConfiguration,
    ) -> ControlDecision:
        if state.risk_level in {"high", "critical"}:
            return ControlDecision(
                action="escalate",
                priority=100,
                rationale=f"Risk level is {state.risk_level}.",
                constraints=["require_human_review"],
            )

        if state.open_items:
            return ControlDecision(
                action="investigate",
                priority=60,
                rationale="There are unresolved operational items.",
                constraints=[],
            )

        action = configuration.rules.get("default_control_action", "continue")
        return ControlDecision(
            action=action,
            priority=10,
            rationale="No high-risk signal or open item requires intervention.",
            constraints=[],
        )


class SkillRouter:
    """Selects a skill from domain and facts."""

    def route(
        self,
        state: OperationalState,
        control_decision: ControlDecision,
    ) -> SkillDecision:
        fact_keys = set(state.facts)
        if state.domain == "wallet" and {"ledger_balance", "provider_balance"} <= fact_keys:
            delta = float(state.facts["provider_balance"]) - float(state.facts["ledger_balance"])
            confidence = 0.95 if delta else 0.8
            return SkillDecision(
                skill_name="wallet_reconciliation",
                confidence=confidence,
                rationale="Wallet balances are available for reconciliation.",
                inputs={"balance_delta": delta},
            )

        if control_decision.action == "escalate":
            return SkillDecision(
                skill_name="incident_triage",
                confidence=0.75,
                rationale="Escalated control action requires triage.",
                inputs={"risk_level": state.risk_level},
            )

        return SkillDecision(
            skill_name="general_operations_review",
            confidence=0.5,
            rationale="No specialized rule matched the state.",
            inputs={},
        )


class PromptModuleRouter:
    """Selects prompt modules that should shape the dynamic prompt."""

    def route(
        self,
        state: OperationalState,
        configuration: OperationalConfiguration,
        control_decision: ControlDecision,
        skill_decision: SkillDecision,
    ) -> list[str]:
        modules = list(configuration.prompt_modules)

        if "summary" not in modules:
            modules.insert(0, "summary")
        if state.open_items and "open_items" not in modules:
            modules.append("open_items")
        if control_decision.action == "escalate" and "risk" not in modules:
            modules.append("risk")
        if skill_decision.skill_name == "wallet_reconciliation" and "reconciliation" not in modules:
            modules.append("reconciliation")

        return modules


class ToolRouter:
    """Selects dependency-free tool names for the next operation."""

    def route(
        self,
        state: OperationalState,
        configuration: OperationalConfiguration,
        skill_decision: SkillDecision,
    ) -> list[str]:
        enabled = set(configuration.enabled_tools)
        selected: list[str] = []

        if skill_decision.skill_name == "wallet_reconciliation":
            selected.extend(tool for tool in ("ledger_lookup", "provider_statement") if tool in enabled)
        if state.open_items and "case_notes" in enabled:
            selected.append("case_notes")
        if state.risk_level in {"high", "critical"} and "alerting" in enabled:
            selected.append("alerting")

        return selected
