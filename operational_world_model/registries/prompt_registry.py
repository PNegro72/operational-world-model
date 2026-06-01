"""Prompt module metadata registry."""

from __future__ import annotations

from typing import TypedDict


class PromptModuleDefinition(TypedDict):
    name: str
    description: str
    module_type: str
    applies_to: list[str]
    path: str


PROMPT_MODULE_REGISTRY: dict[str, PromptModuleDefinition] = {
    "summary": {
        "name": "summary",
        "description": "Generic operational summary.",
        "module_type": "common",
        "applies_to": ["all"],
        "path": "operational_world_model/prompts/common/summary.md",
    },
    "open_items": {
        "name": "open_items",
        "description": "Open operational items.",
        "module_type": "common",
        "applies_to": ["all"],
        "path": "operational_world_model/prompts/common/open_items.md",
    },
    "risk": {
        "name": "risk",
        "description": "Operational risk context.",
        "module_type": "common",
        "applies_to": ["all"],
        "path": "operational_world_model/prompts/common/risk.md",
    },
    "reconciliation": {
        "name": "reconciliation",
        "description": "Wallet reconciliation context.",
        "module_type": "common",
        "applies_to": ["wallet_reconciliation"],
        "path": "operational_world_model/prompts/common/reconciliation.md",
    },
    "pf_context": {
        "name": "pf_context",
        "description": "Plazo Fijo product and reconciliation context.",
        "module_type": "domain_context",
        "applies_to": ["plazo_fijo", "fixed-term"],
        "path": "operational_world_model/prompts/domains/plazo_fijo/pf_context.md",
    },
    "agentic_wh_rules": {
        "name": "agentic_wh_rules",
        "description": "Agentic WH operating rules for planning without executing tools.",
        "module_type": "workflow_rules",
        "applies_to": ["agentic_wh"],
        "path": "operational_world_model/prompts/workflows/plazo_fijo/agentic_wh_rules.md",
    },
    "control_routing_rules": {
        "name": "control_routing_rules",
        "description": "Rules for mapping origins to controls and subcontrols.",
        "module_type": "routing_rules",
        "applies_to": ["control_routing"],
        "path": "operational_world_model/prompts/workflows/plazo_fijo/control_routing_rules.md",
    },
    "sql_generation_rules": {
        "name": "sql_generation_rules",
        "description": "Rules for shaping SQL generation requests.",
        "module_type": "skill_rules",
        "applies_to": ["sql_skill"],
        "path": "operational_world_model/prompts/skills/plazo_fijo/sql_generation_rules.md",
    },
    "analytics_rules": {
        "name": "analytics_rules",
        "description": "Rules for interpreting grouped operational inconsistencies.",
        "module_type": "skill_rules",
        "applies_to": ["analytics_skill"],
        "path": "operational_world_model/prompts/skills/plazo_fijo/analytics_rules.md",
    },
    "core_vs_site_rules": {
        "name": "core_vs_site_rules",
        "description": "Rules for Core versus Site reconciliation controls.",
        "module_type": "subcontrol_rules",
        "applies_to": ["core_vs_site", "conciliaciones_interfaces"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/core_vs_site_rules.md",
    },
    "mov_vs_acc_rules": {
        "name": "mov_vs_acc_rules",
        "description": "Rules for movement versus accounting reconciliation.",
        "module_type": "subcontrol_rules",
        "applies_to": ["mov_vs_acc"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/mov_vs_acc_rules.md",
    },
    "acc_vs_mov_rules": {
        "name": "acc_vs_mov_rules",
        "description": "Rules for accounting versus movement reconciliation.",
        "module_type": "subcontrol_rules",
        "applies_to": ["acc_vs_mov"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/acc_vs_mov_rules.md",
    },
    "bidirectional_rules": {
        "name": "bidirectional_rules",
        "description": "Rules for supported bidirectional reconciliation checks.",
        "module_type": "subcontrol_rules",
        "applies_to": ["bidirectional"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/bidirectional_rules.md",
    },
    "cuenta_puente_rules": {
        "name": "cuenta_puente_rules",
        "description": "Rules for cuenta puente control analysis.",
        "module_type": "subcontrol_rules",
        "applies_to": ["cuenta_puente"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/cuenta_puente_rules.md",
    },
    "roll_forward_rules": {
        "name": "roll_forward_rules",
        "description": "Rules for roll-forward reconciliation analysis.",
        "module_type": "subcontrol_rules",
        "applies_to": ["roll_forward"],
        "path": "operational_world_model/prompts/controls/plazo_fijo/roll_forward_rules.md",
    },
}
