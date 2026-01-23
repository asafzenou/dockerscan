"""Data enrichment functions for package vulnerability scanning."""

from dockerscan.data_packagers_checker.osv_client import OSVClient
from dockerscan.config.logger import Logger


def enrich_packages_with_vulnerabilities(packages: list, os_name: str) -> list:
    """
    Enrich a list of packages with vulnerability data from OSV.dev.
    """
    if not packages:
        Logger().info("No packages to enrich")
        return []

    Logger().info(f"Enriching {len(packages)} packages with vulnerability data...")

    enriched_packages = []
    vuln_count_total = 0

    for idx, package in enumerate(packages, 1):
        package_name = package.get("name")
        package_version = package.get("version")

        if not package_name or not package_version:
            Logger().warning(f"Skipping package with missing name/version: {package}")
            enriched_packages.append(package)
            continue

        Logger().debug(f"[{idx}/{len(packages)}] Checking {package_name}@{package_version}")

        # Query OSV API
        vuln_data = OSVClient.query_vulnerabilities(
            package_name=package_name,
            package_version=package_version,
            os_name=os_name
        )

        # Create enriched package
        enriched_package = {
            "name": package_name,
            "version": package_version,
            "vulnerabilities": {
                "count": vuln_data["count"],
                "items": vuln_data["vulnerabilities"]
            }
        }

        # Add error info if query failed
        if vuln_data.get("error"):
            enriched_package["vulnerabilities"]["error"] = vuln_data["error"]

        enriched_packages.append(enriched_package)

        # Track stats
        if vuln_data["count"] > 0:
            vuln_count_total += vuln_data["count"]
            Logger().warning(
                f"  └─ Found {vuln_data['count']} vulnerability(ies) in {package_name}"
            )
    enriched_packages_sorted = sorted(
        enriched_packages,
        key=lambda p: p["vulnerabilities"]["count"],
        reverse=True
    )

    Logger().info(f"Vulnerability scan complete: {vuln_count_total} total vulnerabilities found")
    return enriched_packages_sorted

