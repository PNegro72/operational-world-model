import unittest

from operational_world_model import (
    OperationalConfiguration,
    OperationalState,
    RuleBasedOperationalWorldModel,
)


class PredictionFlowTests(unittest.TestCase):
    def test_wallet_reconciliation_prediction_flow(self) -> None:
        state = OperationalState(
            state_id="wallet-test",
            domain="wallet",
            facts={"ledger_balance": 10.0, "provider_balance": 7.5},
            open_items=["Review settlement batch"],
        )
        configuration = OperationalConfiguration(
            enabled_tools=["ledger_lookup", "provider_statement", "case_notes"],
            prompt_modules=["summary"],
        )

        trace = RuleBasedOperationalWorldModel().predict(state, configuration)

        self.assertEqual(trace.control_decision.action, "investigate")
        self.assertEqual(trace.skill_decision.skill_name, "wallet_reconciliation")
        self.assertEqual(trace.skill_decision.inputs["balance_delta"], -2.5)
        self.assertIn("reconciliation", trace.selected_prompt_modules)
        self.assertEqual(
            trace.selected_tools,
            ["ledger_lookup", "provider_statement", "case_notes"],
        )
        self.assertEqual(
            trace.predicted_state.facts["reconciliation_status"],
            "requires_adjustment",
        )
        self.assertIn("Reconciliation delta: -2.5", trace.prompt)

    def test_high_risk_state_escalates(self) -> None:
        state = OperationalState(
            state_id="incident-test",
            domain="ops",
            risk_level="critical",
        )
        configuration = OperationalConfiguration(enabled_tools=["alerting"])

        trace = RuleBasedOperationalWorldModel().predict(state, configuration)

        self.assertEqual(trace.control_decision.action, "escalate")
        self.assertEqual(trace.skill_decision.skill_name, "incident_triage")
        self.assertEqual(trace.selected_tools, ["alerting"])
        self.assertTrue(trace.predicted_state.facts["escalation_required"])


if __name__ == "__main__":
    unittest.main()
