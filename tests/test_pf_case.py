import unittest

from operational_world_model import (
    OperationalConfiguration,
    OperationalState,
    RuleBasedOperationalWorldModel,
)


class PlazoFijoCaseTests(unittest.TestCase):
    def test_pf_agentic_wh_routes_to_sql_core_vs_site(self) -> None:
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

        trace = RuleBasedOperationalWorldModel().predict(state, configuration)

        self.assertEqual(trace.skill_decision.skill_name, "sql_skill")
        self.assertIn("vdb_request", trace.selected_tools)
        self.assertIn("sql_skill", trace.selected_tools)
        self.assertIn("bigquery_dry_run", trace.selected_tools)
        self.assertIn("pf_context", trace.selected_prompt_modules)
        self.assertIn("sql_generation_rules", trace.selected_prompt_modules)
        self.assertEqual(trace.predicted_state.facts["suggested_subcontrol"], "core_vs_site")
        self.assertNotIn("bidirectionally", trace.prompt)
        self.assertEqual(trace.predicted_state.facts["query_intent"], "data_query")
        self.assertEqual(trace.predicted_state.facts["analysis_mode"], "grouped_count_by_date")
        self.assertIs(trace.predicted_state.facts["requires_sql"], True)


if __name__ == "__main__":
    unittest.main()
