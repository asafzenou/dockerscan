import sys
from pathlib import Path
from dockerscan.config.logger import Logger
from dockerscan.image_scanner.image_scan_service import ImageScanService
import json
from dockerscan.data_packagers_checker.vulnerability_enrichment_service import VulnerabilityEnrichmentService
from dockerscan.reports.html_output import generate_html_report
import webbrowser

def main(args, parser) -> None:
    """Main CLI entrypoint."""
    scanner = ImageScanService()

    debug = False
    if args.command != "scan":
        parser.print_help()
        sys.exit(1)
    if not debug:
        data = scanner.scan_image(args.image_name)

    if debug:
        output_path = Path("json_debug_os_info.json")
        with open(output_path, "r") as f:
            data = json.load(f)
        data["packages"] = data.get("packages", [])[:5]

    vul_enc = VulnerabilityEnrichmentService(data)
    vul_enc.enrich()
    html_report_path = generate_html_report(vul_enc.get_data(), output_dir=vul_enc.get_html_output_dir())
    Logger().info(f"HTML report generated: {html_report_path.resolve()}")

    # Open the HTML report in the default browser
    try:
        webbrowser.open(f"file:///{html_report_path.resolve()}")
        Logger().info("Opening report in browser...")
    except Exception as e:
        Logger().warning(f"Could not open browser automatically: {e}")







