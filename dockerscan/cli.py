import sys
from pathlib import Path
import tempfile
from dockerscan.config.logger import Logger
from dockerscan.image_scanner.filesystem import Filesystem
from dockerscan.image_scanner.os_detector import OSDetection
from dockerscan.image_scanner.package_scanner import PackageScanner

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
    if args.command != "scan":
        parser.print_help()
        sys.exit(1)
    data = scan_image(args.image_name)



