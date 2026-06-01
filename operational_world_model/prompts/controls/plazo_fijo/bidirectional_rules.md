# Bidirectional Rules

Use only when the selected control is bidirectional or the user explicitly asks for both directions.

Rules:
- Use a `UNION ALL` pattern.
- Movement branch uses `MOVEMENTS_MOV_DATE_CREATED`.
- Accounting branch uses `ACCOUNTING_ACC_MOV_DATE_CREATED`.
- Both branches must return the same columns in the same order.
- Add a `source` column.
- Never mix branch dates.
