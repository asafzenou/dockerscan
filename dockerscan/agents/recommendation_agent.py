from .base import BaseAgent


class RecommendationAgent(BaseAgent):
    """Generate remediation recommendations."""

    def run(self, pkg: dict, analysis: dict, runtime_context: dict) -> dict:
        if analysis.get("false_positive"):
            return {"recommendation": "No action required (false positive)"}

        if not pkg.get("usage_context", {}).get("used_at_runtime"):
            return {
                "recommendation": "Remove package from runtime image (use multi-stage build)"
            }

        if runtime_context.get("user", {}).get("value") == "root":
            return {
                "recommendation": "Run container as non-root user"
            }

        return {
            "recommendation": "Review and update package if applicable"
        }
