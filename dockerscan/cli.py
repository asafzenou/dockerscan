"""CLI entrypoint for dockerscan."""

import argparse
import sys
from pathlib import Path
import tempfile
import shutil

from dockerscan.image_loader import save_and_extract_image
from dockerscan.filesystem import reconstruct_filesystem
from dockerscan.os_detector import detect_os


def scan_image(image_name: str) -> None:
    """Scan a Docker image and detect OS information."""
    print(f"Scanning Docker image: {image_name}")
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_dir = temp_path / "extracted"
        filesystem_dir = temp_path / "filesystem"
        
        print(f"Extracting image to temporary directory...")
        # Save and extract the Docker image
        save_and_extract_image(image_name, extract_dir)
        
        print(f"Reconstructing filesystem from layers...")
        # Reconstruct the merged filesystem
        reconstruct_filesystem(extract_dir, filesystem_dir)
        
        print(f"Detecting OS...")
        # Detect OS from /etc/os-release
        os_info = detect_os(filesystem_dir)
        
        if os_info:
            print(f"Detected OS: {os_info}")
        else:
            print("Could not detect OS from /etc/os-release")
            sys.exit(1)


def main() -> None:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Docker image scanner MVP",
        prog="dockerscan"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    scan_parser = subparsers.add_parser("scan", help="Scan a Docker image")
    scan_parser.add_argument(
        "image_name",
        help="Name of the Docker image to scan (e.g., ubuntu:20.04)"
    )
    
    args = parser.parse_args()
    
    if args.command == "scan":
        scan_image(args.image_name)
    else:
        parser.print_help()
        sys.exit(1)

