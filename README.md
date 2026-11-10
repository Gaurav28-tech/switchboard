# FeaturePilot 🚀

[![CI](https://github.com/Gaurav28-tech/feature-pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/Gaurav28-tech/feature-pilot)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)]()

**FeaturePilot** is a deterministic feature flagging and progressive canary rollout engine engineered for high-availability SaaS and distributed systems. It features stable user-bucketing algorithms, rule-based audience targeting, instant kill-switches, and local evaluation with sub-millisecond execution.

---

## 🚀 Key Features

- **Deterministic Hash Bucketing**: Employs cryptographic SHA-256 bucketing ensuring a user consistently stays in the same rollout bucket (0–100%) across all servers without session affinity.
- **Audience Targeting Rules**: Match user attributes by equality, set inclusion (`in`), regex patterns, or numerical ranges.
- **Instant Kill-Switches**: Master enable/disable flags to neutralize faulty features in production instantly.
- **Local In-Memory Evaluation**: Flags evaluate purely in-process in microseconds without blocking network calls to remote flag servers.
- **Zero Heavy Dependencies**: Pure standard library Python with full type annotations.

---

## 🏗️ Architecture

```
User Context: { id: "usr_481", plan: "enterprise", region: "eu-west" }
                     |
                     v
+--------------------------------------------------------+
| FeaturePilot Evaluation Engine                         |
|                                                        |
|   1. Master Kill-Switch Check                          |
|   2. Whitelist / Forced Override Match                 |
|   3. Audience Targeting Rules (plan == 'enterprise')   |
|   4. Deterministic Hash Bucketing (hash % 100 < 25%)   |
+--------------------------------------------------------+
                     |
                     v
Result: True (Feature Enabled) / False (Fallback)
```

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Gaurav28-tech/feature-pilot.git
cd feature-pilot
```

### Basic Usage

```python
from pilot.client import FeaturePilot
from pilot.models import FeatureFlag, TargetingRule

client = FeaturePilot()

# Define a 20% canary rollout flag for beta search
flag = FeatureFlag(
    key="ai-search-v2",
    description="Next-gen semantic vector search",
    enabled=True,
    rollout_percentage=20, # 20% of all users
    rules=[
        TargetingRule(attribute="tier", operator="equals", value="enterprise") # Always on for enterprise
    ]
)
client.register_flag(flag)

# Evaluate flag for a user
is_enabled = client.is_enabled(
    flag_key="ai-search-v2",
    user_id="usr_9812",
    attributes={"tier": "enterprise"}
)
print(f"Feature Enabled: {is_enabled}")
```

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
