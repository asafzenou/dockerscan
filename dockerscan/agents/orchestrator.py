from .vulnerability_agent import VulnerabilityAgent
from .runtime_agent import RuntimeAgent
from .risk_agent import RiskAgent
from .false_positive_agent import FalsePositiveAgent
from .recommendation_agent import RecommendationAgent


class AnalysisOrchestrator:
    """Coordinate all agents to analyze a package."""

    def __init__(self):
        self.vuln_agent = VulnerabilityAgent()
        self.runtime_agent = RuntimeAgent()
        self.risk_agent = RiskAgent()
        self.fp_agent = FalsePositiveAgent()
        self.recommendation_agent = RecommendationAgent()

    def analyze_package(self, pkg: dict, os_info: dict, runtime_context: dict) -> dict:
        analysis = {}

        vulnerabilities = pkg.get("vulnerabilities", {})
        items = vulnerabilities.get("items", [])

        if not items:
            return {"analysis": {"effective_risk": "NONE"}}

        vuln = items[0]  # MVP: first vulnerability

        analysis.update(self.vuln_agent.run(vulnerabilities))
        analysis.update(self.runtime_agent.run(pkg.get("usage_context", {}), runtime_context))
        analysis.update(self.fp_agent.run(os_info, vuln))
        analysis.update(self.risk_agent.run(vuln, pkg.get("usage_context", {}), runtime_context))
        analysis.update(self.recommendation_agent.run(pkg, analysis, runtime_context))

        return {"analysis": analysis}
