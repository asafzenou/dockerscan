import argparse
from dockerscan.cli import main

def run():
    parser = argparse.ArgumentParser(
        description="Docker image scanner",
        prog="dockerscan"
    )

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan a Docker image")
    scan_parser.add_argument(
        "image_name",
        help="Name of the Docker image to scan (e.g., ubuntu:20.04)"
    )

    args = parser.parse_args()
    main(args, parser)

if __name__ == "__main__":
    run()
