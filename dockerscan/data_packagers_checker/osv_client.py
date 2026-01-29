"""OSV.dev API client for vulnerability enrichment."""

import requests
from typing import Optional
from dockerscan.config.logger import Logger


class OSVClient:
    """Client for querying OSV.dev vulnerability database."""

    API_URL = "https://api.osv.dev/v1/query"
    API_DETAIL_URL = "https://osv.dev/vulnerability/"
    TIMEOUT = 10  # seconds

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

            enriched_vulns = []

            for vuln in vulns:
                patch_info = OSVClient._extract_patch_info(vuln, package_version)
                affected_meta = OSVClient._extract_affected_metadata(vuln)

                enriched_vulns.append({
                    "id": vuln.get("id", "UNKNOWN"),
                    "summary": vuln.get("summary", "No summary available"),
                    "severity": OSVClient._extract_severity(vuln),
                    "patch_status": patch_info["patch_status"],
                    "fixed_version": patch_info["fixed_version"],
                    "affected_ecosystem": affected_meta.get("affected_ecosystem"),
                    "urgency": affected_meta.get("urgency"),
                    "versions": affected_meta.get("versions"),
                    "published": vuln.get("published"),
                    "modified": vuln.get("modified"),
                    "references": affected_meta.get("references"),
                    "upstream": vuln.get("upstream", []),
                    "details_url": f"{OSVClient.API_DETAIL_URL}{vuln.get('id', '')}" # UX
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

    @staticmethod
    def _extract_patch_info(vuln: dict, installed_version: str) -> dict:
        """
        Extract patch status and fixed version from OSV vulnerability data.
        """
        fixed_versions = []

        for affected in vuln.get("affected", []):
            for r in affected.get("ranges", []):
                for event in r.get("events", []):
                    if "fixed" in event:
                        fixed_versions.append(event["fixed"])

        if not fixed_versions:
            return {
                "patch_status": "UNKNOWN",
                "fixed_version": None
            }

        for fixed in fixed_versions:
            if installed_version >= fixed:
                return {
                    "patch_status": "PATCHED",
                    "fixed_version": fixed
                }

        return {
            "patch_status": "UNPATCHED",
            "fixed_version": fixed_versions[0]
        }

    @staticmethod
    def _extract_affected_metadata(vuln: dict) -> dict:
        """
        Extract relevant metadata from OSV 'affected' entries.
        """
        affected_entries = vuln.get("affected", [])
        if not affected_entries:
            return {}

        affected = affected_entries[0]

        return {
            "affected_ecosystem": affected.get("package", {}).get("ecosystem"),
            "urgency": affected.get("ecosystem_specific", {}).get("urgency"),
            "versions": affected.get("versions", []),
            "references": [ref.get("url") for ref in vuln.get("references", [])]
        }



