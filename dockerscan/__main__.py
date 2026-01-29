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

# import argparse
#
# from dockerscan.cli import main as legacy_main
# from dockerscan.cli_agentic import main as agentic_main
#
#
# def run():
#     parser = argparse.ArgumentParser(
#         prog="dockerscan",
#         description="Docker image security scanner"
#     )
#
#     subparsers = parser.add_subparsers(dest="command", required=True)
#
#     # ----------------------------
#     # Legacy deterministic scan
#     # ----------------------------
#     scan_parser = subparsers.add_parser(
#         "scan",
#         help="Run deterministic vulnerability scan"
#     )
#     scan_parser.add_argument(
#         "image_name",
#         help="Docker image name (e.g. ubuntu:20.04)"
#     )
#
#     # ----------------------------
#     # Agentic scan
#     # ----------------------------
#     agentic_parser = subparsers.add_parser(
#         "scan-agentic",
#         help="Run agent-based reasoning scan"
#     )
#     agentic_parser.add_argument(
#         "image_name",
#         help="Docker image name (e.g. ubuntu:20.04)"
#     )
#
#     args = parser.parse_args()
#
#     if args.command == "scan":
#         legacy_main(args)
#     elif args.command == "scan-agentic":
#         agentic_main(args)
#
#
# if __name__ == "__main__":
#     run()
