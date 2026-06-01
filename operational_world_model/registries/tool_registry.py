"""Tool metadata registry.

The OWM only selects tool names. It does not execute tools.
"""

from __future__ import annotations

from typing import TypedDict


class ToolDefinition(TypedDict):
    name: str
    description: str
    type: str
    required_by_default: bool


TOOL_REGISTRY: dict[str, ToolDefinition] = {
    "vdb_request": {
        "name": "vdb_request",
        "description": "Retrieve contextual control knowledge from a vector database.",
        "type": "retrieval",
        "required_by_default": True,
    },
    "sql_skill": {
        "name": "sql_skill",
        "description": "Generate SQL intent for data questions.",
        "type": "skill",
        "required_by_default": True,
    },
    "bigquery_dry_run": {
        "name": "bigquery_dry_run",
        "description": "Validate BigQuery SQL shape and estimated execution without running it.",
        "type": "validation",
        "required_by_default": True,
    },
    "analytics_skill": {
        "name": "analytics_skill",
        "description": "Analyze result sets and produce operational findings.",
        "type": "skill",
        "required_by_default": False,
    },
    "export2file": {
        "name": "export2file",
        "description": "Export generated artifacts or findings to a file.",
        "type": "export",
        "required_by_default": False,
    },
    "control_registry": {
        "name": "control_registry",
        "description": "Lookup control and subcontrol definitions.",
        "type": "registry",
        "required_by_default": False,
    },
    "field_dictionary": {
        "name": "field_dictionary",
        "description": "Lookup canonical field names and meanings.",
        "type": "metadata",
        "required_by_default": False,
    },
    "control_examples": {
        "name": "control_examples",
        "description": "Retrieve examples for similar controls.",
        "type": "retrieval",
        "required_by_default": False,
    },
    "get_table_definition_bq": {
        "name": "get_table_definition_bq",
        "description": "Retrieve BigQuery table definitions for candidate datasets.",
        "type": "metadata",
        "required_by_default": False,
    },
}
