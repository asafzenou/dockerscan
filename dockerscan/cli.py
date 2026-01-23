import sys
from pathlib import Path
from dockerscan.config.logger import Logger
from dockerscan.image_scanner.image_scan_service import ImageScanService
import json
from dockerscan.data_packagers_checker import enrich_packages_with_vulnerabilities
from dockerscan.html_output import generate_html_report
from datetime import datetime
import webbrowser

def main(args, parser) -> None:
    """Main CLI entrypoint."""
    scanner = ImageScanService()
    debug = True
    if args.command != "scan":
        parser.print_help()
        sys.exit(1)
    if not debug:
        data = scanner.scan_image(args.image_name)
    if debug:
        output_path = Path("json_debug_os_info.json")
        with open(output_path, "r") as f:
            data = json.load(f)

    # Enrich packages with vulnerability data
    os_name = data.get("os_info", {}).get("name", "Unknown")
    os_version = data.get("os_info", {}).get("version", "unknown")
    packages = data.get("packages", [])

    Logger().info(f"Starting vulnerability enrichment for {os_name}...")
    enriched_packages = enrich_packages_with_vulnerabilities(packages, os_name)
    data["packages"] = enriched_packages
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os_version_clean = os_version.replace(":", "_").replace("/", "_").replace(" ", "_")
    html_output_dir = Path("html_reports") / f"{os_name}_{os_version_clean}_{timestamp}"

    html_report_path = generate_html_report(data, output_dir=html_output_dir)
    Logger().info(f"HTML report generated: {html_report_path.resolve()}")

    # Open the HTML report in the default browser
    try:
        webbrowser.open(f"file:///{html_report_path.resolve()}")
        Logger().info("Opening report in browser...")
    except Exception as e:
        Logger().warning(f"Could not open browser automatically: {e}")







