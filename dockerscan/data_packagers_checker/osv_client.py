"""OSV.dev API client for vulnerability enrichment."""

import requests
from typing import Optional
from dockerscan.config.logger import Logger


class OSVClient:
    """Client for querying OSV.dev vulnerability database."""

    API_URL = "https://api.osv.dev/v1/query"
    TIMEOUT = 10  # seconds

    # Map OS names to OSV ecosystems
    ECOSYSTEM_MAP = {
        "debian": "Debian",
        "debian gnu/linux": "Debian",
        "ubuntu": "Debian",  # Ubuntu uses Debian packages
        "red hat enterprise linux": "Red Hat",
        "rhel": "Red Hat",
        "centos": "Red Hat",
        "alpine": "Alpine",
        "alpine linux": "Alpine"
    }

    @staticmethod
    def get_ecosystem(os_name: str) -> Optional[str]:
        """Map OS name to OSV ecosystem."""
        if not os_name:
            return None

        os_lower = os_name.lower().strip()
        return OSVClient.ECOSYSTEM_MAP.get(os_lower)

    @staticmethod
    def query_vulnerabilities(package_name: str, package_version: str, os_name: str) -> dict:
        """
        Query OSV.dev API for vulnerabilities in a specific package version.

        Args:
            package_name: Name of the package (e.g., "bash")
            package_version: Version string (e.g., "5.2.15-2+b7")
            os_name: OS name (e.g., "Debian GNU/Linux")

        Returns:
            dict with:
                - "vulnerabilities": list of CVE objects
                - "count": number of vulnerabilities found
                - "error": error message if request failed
        """
        ecosystem = OSVClient.get_ecosystem(os_name)

        if not ecosystem:
            return {
                "vulnerabilities": [],
                "count": 0,
                "error": f"Unsupported OS for vulnerability scanning: {os_name}"
            }

        # Build OSV query payload
        payload = {
            "package": {
                "name": package_name,
                "ecosystem": ecosystem
            },
            "version": package_version
        }

        try:
            response = requests.post(
                OSVClient.API_URL,
                json=payload,
                timeout=OSVClient.TIMEOUT
            )
            response.raise_for_status()

            data = response.json()
            vulns = data.get("vulns", [])

            # Extract relevant fields
            enriched_vulns = []
            for vuln in vulns:
                enriched_vulns.append({
                    "id": vuln.get("id", "UNKNOWN"),
                    "summary": vuln.get("summary", "No summary available"),
                    "severity": OSVClient._extract_severity(vuln),
                    "details_url": f"https://osv.dev/vulnerability/{vuln.get('id', '')}"
                })

            return {
                "vulnerabilities": enriched_vulns,
                "count": len(enriched_vulns),
                "error": None
            }

        except requests.exceptions.Timeout:
            Logger().warning(f"OSV API timeout for {package_name}@{package_version}")
            return {
                "vulnerabilities": [],
                "count": 0,
                "error": "API timeout"
            }
        except requests.exceptions.RequestException as e:
            Logger().warning(f"OSV API error for {package_name}@{package_version}: {e}")
            return {
                "vulnerabilities": [],
                "count": 0,
                "error": str(e)
            }
        except Exception as e:
            Logger().error(f"Unexpected error querying OSV for {package_name}: {e}")
            return {
                "vulnerabilities": [],
                "count": 0,
                "error": f"Unexpected error: {str(e)}"
            }

    @staticmethod
    def _extract_severity(vuln: dict) -> Optional[str]:
        """Extract severity rating from vulnerability data."""
        try:
            # OSV stores severity in different formats
            severity_list = vuln.get("severity", [])
            if severity_list and len(severity_list) > 0:
                # Try to get CVSS score
                for sev in severity_list:
                    if sev.get("type") == "CVSS_V3":
                        score = sev.get("score")
                        if score:
                            return f"CVSS: {score}"

            # Fallback to database-specific severity
            if vuln.get("database_specific"):
                db_severity = vuln["database_specific"].get("severity")
                if db_severity:
                    return db_severity

            return None
        except Exception:
            return None

