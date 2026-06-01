"""Run a minimal wallet reconciliation example."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operational_world_model import (
    OperationalConfiguration,
    OperationalState,
    RuleBasedOperationalWorldModel,
)


def main() -> None:
    state = OperationalState(
        state_id="wallet-2026-06-01",
        domain="wallet",
        facts={
            "ledger_balance": 1000.0,
            "provider_balance": 997.5,
            "currency": "USD",
        },
        signals=["daily_close"],
        risk_level="normal",
        open_items=["Investigate provider settlement delta"],
    )
    configuration = OperationalConfiguration(
        name="wallet-mvp",
        enabled_tools=["ledger_lookup", "provider_statement", "case_notes"],
        prompt_modules=["summary"],
    )

    model = RuleBasedOperationalWorldModel()
    trace = model.predict(state, configuration)

    print("Control decision:", trace.control_decision)
    print("Skill decision:", trace.skill_decision)
    print("Selected tools:", trace.selected_tools)
    print("Predicted facts:", trace.predicted_state.facts)
    print("\nPrompt:\n")
    print(trace.prompt)


if __name__ == "__main__":
    main()
