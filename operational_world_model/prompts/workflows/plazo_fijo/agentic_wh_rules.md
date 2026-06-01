# Agentic WH Rules

Source workflow: CT_PlazoFijo_Agentic_WH.

The original workflow starts with VDB Request to retrieve context before deciding how to proceed.
The OWM does not execute tools; it only selects the tools and prompt modules that should be used later.

Classify the user intent as one of:
- data_query
- analytical_query
- functional_explanation
- follow_up_export

For data queries:
- Use SQL Skill.
- Then use BigQuery Dry-Run to validate the generated query.
- Do not generate SQL directly in the Agentic WH workflow. SQL must come from SQL Skill.

For analytical queries:
- Use Analytics Skill.
- If data is missing, request SQL through SQL Skill.

Final response format in the real workflow:
- Executive summary.
- Explanation.
- Results table, if applicable.
- SQL used.
- Sources.
