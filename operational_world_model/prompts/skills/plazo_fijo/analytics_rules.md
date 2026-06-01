# Analytics Rules

Source workflow: CT_PlazoFijo_Analytics_Skill.

Analytics Skill diagnoses drops, reconciliation failures, trend changes, drivers, and comparisons.
It must not generate SQL.
It must not execute queries.
It must use `already_executed_results` first.

Rules:
- Always consult control registry.
- Use control examples and field dictionary only when useful.
- If data is insufficient, request the minimum `queries_needed`.
- Do not invent causes.

Output is structured around:
- analysis_type
- metric
- comparison_strategy
- dimensions_to_analyze
- hypotheses
- findings
- queries_needed
- confidence
