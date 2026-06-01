# Control Routing Rules

Source routing: VerdiCode routing.

Normalize `control_origin` before routing.
`Conciliaciones: Interfaces` maps to parent control `conciliaciones_interfaces`.

Possible subcontrols:
- core_vs_site
- movements_vs_accounting
- accounting_vs_movements
- bidirectional

Use aliases, phrases, keywords, semantic patterns, and negative patterns.
If score is high and the gap is enough, resolve the subcontrol.
If the route is ambiguous, keep the parent control and set `routing_status` to `ambiguous`.

Trace fields to produce:
- suggested_subcontrol
- confidence
- routing_status
- routing_note

Current suggested subcontrol: {{suggested_subcontrol}}
