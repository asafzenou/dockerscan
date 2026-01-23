from pathlib import Path
import tempfile
import sys

from dockerscan.config.logger import Logger
from dockerscan.image_scanner.filesystem import Filesystem
from dockerscan.image_scanner.package_scanner import PackageScanner
from dockerscan.image_scanner.os_detector import OSDetection


class ImageScanService:
    def __init__(self):
        self.logger = Logger()
        self.filesystem = Filesystem()
        self.package_scanner = PackageScanner()

    def from_docker_to_dir(self,image_name: str,extract_dir: Path,filesystem_dir: Path) -> None:
        self.logger.info("Extracting image to temporary directory...")
        self.filesystem.save_and_extract_image(image_name, extract_dir)
        self.filesystem.reconstruct_filesystem(extract_dir, filesystem_dir)

    def get_packages(self, filesystem_dir: Path, os_info) -> list:
        self.logger.info("Scanning packages...")
        result = self.package_scanner.scan(filesystem_dir, os_info)
        packages = result.get("packages", [])
        self.logger.info(f"Found {len(packages)} installed packages")
        return packages

    def scan_image(self, image_name: str) -> dict:
        """
        Scan a Docker image and return OS info + installed packages.
        """
        self.logger.info(f"Scanning Docker image: {image_name}")
        data = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            extract_dir = temp_path / "extracted"
            filesystem_dir = temp_path / "filesystem"

            self.from_docker_to_dir(image_name, extract_dir, filesystem_dir)

            self.logger.info("Detecting OS...")
            os_info = OSDetection.detect_os(filesystem_dir)

            if not os_info:
                self.logger.error("Could not detect OS from /etc/os-release")
                sys.exit(1)

            self.logger.info(f"Detected OS: {os_info}")
            data["os_info"] = os_info

            packages = self.get_packages(filesystem_dir, OSDetection.get_os())
            data["packages"] = packages

        self.logger.info("Scan complete.")
        return data
