from .base import BaseAgent


class RiskAgent(BaseAgent):
    """Calculate effective risk based on multiple factors."""

    def run(self, vuln: dict, usage_context: dict, runtime_context: dict) -> dict:
        score = 0
        severity = vuln.get("severity", "")

        if "C:H" in severity or "I:H" in severity or "A:H" in severity:
            score += 3
        elif "C:M" in severity or "I:M" in severity:
            score += 2
        else:
            score += 1

        if usage_context.get("used_at_runtime"):
            score += 2

        if runtime_context.get("user", {}).get("value") == "root":
            score += 1

        if vuln.get("patch_status") == "PATCHED":
            score -= 1

        if score >= 4:
            level = "HIGH"
        elif score >= 2:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "effective_risk": level,
            "risk_score": score
        }
