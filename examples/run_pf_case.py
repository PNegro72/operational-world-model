"""Run the first Plazo Fijo Agentic WH case."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operational_world_model import (  # noqa: E402
    OperationalConfiguration,
    OperationalState,
    RuleBasedOperationalWorldModel,
)


def main() -> None:
    state = OperationalState(
        state_id="pf_case_001",
        domain="plazo_fijo",
        facts={
            "question": "que fecha contiene más incosistencias en el mes de enero 2026?",
            "control_origin": "Conciliaciones: Interfaces",
            "product": "fixed-term",
            "parent_control": "conciliaciones_interfaces",
        },
        signals=["fecha", "incosistencias", "enero", "2026"],
        risk_level="normal",
        open_items=[],
    )
    configuration = OperationalConfiguration(
        name="pf-agentic-wh",
        enabled_tools=[
            "vdb_request",
            "sql_skill",
            "bigquery_dry_run",
            "analytics_skill",
            "export2file",
        ],
        prompt_modules=[
            "pf_context",
            "agentic_wh_rules",
            "control_routing_rules",
        ],
    )

    model = RuleBasedOperationalWorldModel()
    trace = model.predict(state, configuration)

    print("Control decision:", trace.control_decision)
    print("Skill decision:", trace.skill_decision)
    print("Selected tools:", trace.selected_tools)
    print("Selected prompt modules:", trace.selected_prompt_modules)
    print("Predicted facts:", trace.predicted_state.facts)
    print("Query intent:", trace.predicted_state.facts.get("query_intent"))
    print("Analysis mode:", trace.predicted_state.facts.get("analysis_mode"))
    print("Requires SQL:", trace.predicted_state.facts.get("requires_sql"))
    print("Predicted state:", trace.predicted_state)
    print("\nGenerated prompt:\n")
    print(trace.prompt)


if __name__ == "__main__":
    main()
