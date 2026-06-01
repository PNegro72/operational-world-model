"""Prompt module metadata registry."""

from __future__ import annotations

from typing import TypedDict


class PromptModuleDefinition(TypedDict):
    name: str
    description: str
    applies_to: list[str]
    module_type: str


PROMPT_MODULE_REGISTRY: dict[str, PromptModuleDefinition] = {
    "pf_context": {
        "name": "pf_context",
        "description": "Plazo Fijo product and reconciliation context.",
        "applies_to": ["plazo_fijo", "fixed-term"],
        "module_type": "domain_context",
    },
    "agentic_wh_rules": {
        "name": "agentic_wh_rules",
        "description": "Agentic WH operating rules for planning without executing tools.",
        "applies_to": ["agentic_wh"],
        "module_type": "workflow_rules",
    },
    "control_routing_rules": {
        "name": "control_routing_rules",
        "description": "Rules for mapping origins to controls and subcontrols.",
        "applies_to": ["control_routing"],
        "module_type": "routing_rules",
    },
    "sql_generation_rules": {
        "name": "sql_generation_rules",
        "description": "Rules for shaping SQL generation requests.",
        "applies_to": ["sql_skill"],
        "module_type": "skill_rules",
    },
    "analytics_rules": {
        "name": "analytics_rules",
        "description": "Rules for interpreting grouped operational inconsistencies.",
        "applies_to": ["analytics_skill"],
        "module_type": "skill_rules",
    },
    "core_vs_site_rules": {
        "name": "core_vs_site_rules",
        "description": "Rules for Core versus Site reconciliation controls.",
        "applies_to": ["core_vs_site", "conciliaciones_interfaces"],
        "module_type": "subcontrol_rules",
    },
    "mov_vs_acc_rules": {
        "name": "mov_vs_acc_rules",
        "description": "Rules for movement versus account reconciliation.",
        "applies_to": ["mov_vs_acc"],
        "module_type": "subcontrol_rules",
    },
    "acc_vs_mov_rules": {
        "name": "acc_vs_mov_rules",
        "description": "Rules for account versus movement reconciliation.",
        "applies_to": ["acc_vs_mov"],
        "module_type": "subcontrol_rules",
    },
    "bidirectional_rules": {
        "name": "bidirectional_rules",
        "description": "Rules for bidirectional reconciliation checks.",
        "applies_to": ["bidirectional"],
        "module_type": "subcontrol_rules",
    },
    "cuenta_puente_rules": {
        "name": "cuenta_puente_rules",
        "description": "Rules for cuenta puente control analysis.",
        "applies_to": ["cuenta_puente"],
        "module_type": "subcontrol_rules",
    },
    "roll_forward_rules": {
        "name": "roll_forward_rules",
        "description": "Rules for roll-forward reconciliation analysis.",
        "applies_to": ["roll_forward"],
        "module_type": "subcontrol_rules",
    },
}
