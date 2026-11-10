import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pilot.models import FeatureFlag, TargetingRule
from pilot.client import FeaturePilot
from pilot.bucketing import HashBucket

class TestFeaturePilot(unittest.TestCase):
    def setUp(self):
        self.pilot = FeaturePilot()

    def test_deterministic_bucketing(self):
        b1 = HashBucket.calculate_bucket("flag-1", "user-100")
        b2 = HashBucket.calculate_bucket("flag-1", "user-100")
        self.assertEqual(b1, b2)
        self.assertTrue(0 <= b1 < 100)

    def test_master_killswitch(self):
        flag = FeatureFlag(key="new-checkout", description="test", enabled=False, rollout_percentage=100)
        self.pilot.register_flag(flag)
        self.assertFalse(self.pilot.is_enabled("new-checkout", user_id="u1"))

    def test_targeting_rules(self):
        flag = FeatureFlag(
            key="beta-dashboard",
            description="Beta UI",
            enabled=True,
            rollout_percentage=0,
            rules=[TargetingRule(attribute="role", operator="equals", value="admin")]
        )
        self.pilot.register_flag(flag)

        self.assertTrue(self.pilot.is_enabled("beta-dashboard", attributes={"role": "admin"}))
        self.assertFalse(self.pilot.is_enabled("beta-dashboard", attributes={"role": "member"}))

    def test_overrides(self):
        flag = FeatureFlag(
            key="dark-mode",
            description="theme",
            enabled=True,
            rollout_percentage=0,
            overrides={"vip_user": True}
        )
        self.pilot.register_flag(flag)
        self.assertTrue(self.pilot.is_enabled("dark-mode", user_id="vip_user"))
        self.assertFalse(self.pilot.is_enabled("dark-mode", user_id="normal_user"))

if __name__ == "__main__":
    unittest.main()
