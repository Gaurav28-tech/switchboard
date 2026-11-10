from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict, Optional

class RuleOperator(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    IN = "in"
    GREATER_THAN = "greater_than"

@dataclass
class TargetingRule:
    attribute: str
    operator: str  # e.g. "equals", "in"
    value: Any

@dataclass
class FeatureFlag:
    key: str
    description: str
    enabled: bool = True
    rollout_percentage: int = 100  # 0 to 100
    rules: List[TargetingRule] = field(default_factory=list)
    overrides: Dict[str, bool] = field(default_factory=dict)
