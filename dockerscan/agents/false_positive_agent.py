from .base import BaseAgent


class FalsePositiveAgent(BaseAgent):
    """Detect likely false positives (e.g., Debian backports)."""

    def run(self, os_info: dict, vuln: dict) -> dict:
        os_name = os_info.get("name", "").lower()

        if os_name.startswith("debian") and vuln.get("patch_status") == "PATCHED":
            return {
                "false_positive": True,
                "reason": "Debian backported patch applied"
            }

        return {
            "false_positive": False
        }
