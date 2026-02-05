from typing import Dict

_profiles: Dict[str, Dict] = {}

def get_profile(session: str, user: str) -> Dict:
    key = f"{session}:{user}"
    if key not in _profiles:
        _profiles[key] = {"style": "concise", "bias": {}}
    return _profiles[key]

def apply_correction(profile: Dict, incorrect: str, correct: str):
    bias = profile.setdefault("bias", {})
    bias[correct] = bias.get(correct, 0) + 1
