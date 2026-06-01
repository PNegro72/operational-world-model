# SQL Generation Rules

Source workflow: CT_PlazoFijo_SQL_Skill.

SQL Skill only generates BigQuery SQL.
It must not explain business results.

It must use:
- control registry
- field dictionary, if needed
- control examples, if needed
- get table definition bq

Rules:
- Always consult control registry.
- Validate schema before using columns.
- Do not invent tables or columns.
- Use `default_filters` and `special_rules` from the registry.
- Respect `mandatory_partitioning_field`.
- Use `DATE()` for date conversions when appropriate.
- Return valid JSON only in the real workflow.

For this OWM trace:
- Query intent: {{query_intent}}
- Grouping field: {{group_by}}
- Metric: {{metric}}
