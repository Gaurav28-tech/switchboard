from typing import Dict, Any, Optional
from pilot.models import FeatureFlag
from pilot.bucketing import HashBucket
from pilot.evaluator import RuleEvaluator

class FeaturePilot:
    def __init__(self):
        self.flags: Dict[str, FeatureFlag] = {}

    def register_flag(self, flag: FeatureFlag):
        self.flags[flag.key] = flag

    def is_enabled(self, flag_key: str, user_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None, default: bool = False) -> bool:
        if flag_key not in self.flags:
            return default

        flag = self.flags[flag_key]

        # 1. Master killswitch
        if not flag.enabled:
            return False

        # 2. Explicit overrides
        if user_id and user_id in flag.overrides:
            return flag.overrides[user_id]

        attrs = attributes or {}

        # 3. Rule matching
        for rule in flag.rules:
            if RuleEvaluator.evaluate_rule(rule, attrs):
                return True

        # 4. Percentage rollout
        if flag.rollout_percentage <= 0:
            return False
        if flag.rollout_percentage >= 100:
            return True

        if not user_id:
            return False

        bucket = HashBucket.calculate_bucket(flag.key, user_id)
        return bucket < flag.rollout_percentage
