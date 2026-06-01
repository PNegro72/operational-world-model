"""Dataclass schemas used by the operational world model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OperationalState:
    """A snapshot of an operational situation."""

    state_id: str
    domain: str
    facts: dict[str, Any] = field(default_factory=dict)
    signals: list[str] = field(default_factory=list)
    risk_level: str = "normal"
    open_items: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class OperationalConfiguration:
    """Runtime configuration for rule-based operational decisions."""

    name: str = "default"
    rules: dict[str, str] = field(default_factory=dict)
    thresholds: dict[str, float] = field(default_factory=dict)
    enabled_tools: list[str] = field(default_factory=list)
    prompt_modules: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ControlDecision:
    """Decision about the next operational control action."""

    action: str
    priority: int
    rationale: str
    constraints: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SkillDecision:
    """Decision about the operational skill to apply."""

    skill_name: str
    confidence: float
    rationale: str
    inputs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OperationalTrace:
    """Complete trace of one model prediction."""

    state: OperationalState
    configuration: OperationalConfiguration
    control_decision: ControlDecision
    skill_decision: SkillDecision
    selected_prompt_modules: list[str]
    selected_tools: list[str]
    prompt: str
    predicted_state: OperationalState
    notes: list[str] = field(default_factory=list)
