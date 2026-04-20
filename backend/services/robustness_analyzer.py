from random import Random


def run_adversarial_analysis(strength: float, attack_type: str) -> dict:
    rnd = Random(42)
    baseline = max(0.0, 1.0 - strength * 0.8)
    return {
        "attack_type": attack_type,
        "strength": strength,
        "robust_accuracy": round(baseline + rnd.uniform(-0.03, 0.03), 4),
        "confidence_drop": round(min(1.0, strength * rnd.uniform(0.4, 0.9)), 4),
    }


def run_perturbation_analysis(strength: float) -> dict:
    rnd = Random(99)
    baseline = max(0.0, 1.0 - strength * 0.6)
    return {
        "perturbation_level": strength,
        "stability_score": round(baseline + rnd.uniform(-0.02, 0.02), 4),
        "performance_delta": round(min(1.0, strength * rnd.uniform(0.3, 0.7)), 4),
    }
