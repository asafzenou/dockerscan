import sys
from pathlib import Path
import tempfile
from dockerscan.config.logger import Logger
from dockerscan.image_scanner.filesystem import Filesystem
from dockerscan.image_scanner.os_detector import OSDetection
from dockerscan.image_scanner.package_scanner import PackageScanner
import json
from dockerscan.data_packagers import enrich_packages_with_vulnerabilities
from dockerscan.html_output import generate_html_report
from datetime import datetime
import webbrowser

def from_docker_to_dir(image_name: str, extract_dir: Path,filesystem_dir: Path) -> None:
    Logger().info(f"Extracting image to temporary directory...")
    filesystem = Filesystem()
    filesystem.save_and_extract_image(image_name, extract_dir)
    filesystem.reconstruct_filesystem(extract_dir, filesystem_dir)

def get_packages(filesystem_dir: Path, os_info) -> list:
    Logger().info(f"Scanning packages...")
    scanner = PackageScanner()
    result = scanner.scan(filesystem_dir, os_info)
    packages = result.get("packages", [])
    Logger().info(f"Found {len(packages)} installed packages")
    return packages

def scan_image(image_name: str) -> dict:
    """Scan a Docker image and detect OS information."""
    Logger().info(f"Scanning Docker image: {image_name}")
    data = {}
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_dir = temp_path / "extracted"
        filesystem_dir = temp_path / "filesystem"

        from_docker_to_dir(image_name, extract_dir, filesystem_dir)

        Logger().info(f"Detecting OS...")
        os_info = OSDetection.detect_os(filesystem_dir) # name, version

        if not os_info:
            Logger().error("Could not detect OS from /etc/os-release")
            sys.exit(1)
        Logger().info(f"Detected OS: {os_info}")
        data["os_info"] = os_info
        packages = get_packages(filesystem_dir, OSDetection.get_os())
        data["packages"] = packages
    Logger().info("Scan complete.")
    return data

def main(args, parser) -> None:
    """Main CLI entrypoint."""
    debug = True
    if args.command != "scan":
        parser.print_help()
        sys.exit(1)
    if not debug:
        data = scan_image(args.image_name)
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







