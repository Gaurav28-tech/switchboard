from typing import Dict, Any
from pilot.models import TargetingRule, RuleOperator

class RuleEvaluator:
    @staticmethod
    def evaluate_rule(rule: TargetingRule, attributes: Dict[str, Any]) -> bool:
        if rule.attribute not in attributes:
            return False

        attr_val = attributes[rule.attribute]
        op = rule.operator.lower()

        if op == "equals":
            return attr_val == rule.value
        elif op == "not_equals":
            return attr_val != rule.value
        elif op == "contains":
            return str(rule.value) in str(attr_val)
        elif op == "in":
            return attr_val in rule.value if isinstance(rule.value, (list, set, tuple)) else False
        elif op == "greater_than":
            try:
                return float(attr_val) > float(rule.value)
            except (ValueError, TypeError):
                return False

        return False
