from .base import BaseAgent


class RuntimeAgent(BaseAgent):
    """Analyze runtime exposure of a package."""

    def run(self, usage_context: dict, runtime_context: dict) -> dict:
        return {
            "used_at_runtime": usage_context.get("used_at_runtime", False),
            "runs_as_root": runtime_context.get("user", {}).get("value") == "root"
        }
