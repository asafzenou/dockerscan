from pathlib import Path
from dockerscan.config.os_packages import OS_PACKAGE_CONFIG
from dockerscan.parsers import PACKAGE_PARSERS
from dockerscan.logger import Logger


class PackageScanner:
    """Scan and extract OS packages from a Docker image filesystem."""

    def scan(self, filesystem_dir: Path, os_name: str) -> list[dict]:
        os_config = self._get_os_config(os_name)
        if not os_config:
            return []

        parser = self._get_parser(os_name, os_config)
        if not parser:
            return []

        return self._scan_package_databases(
            filesystem_dir,
            os_name,
            os_config["db_files"],
            parser,
        )

    # ───────────────────────── helpers ─────────────────────────

    def _get_os_config(self, os_name: str) -> dict | None:
        os_key = os_name.lower()
        config = OS_PACKAGE_CONFIG.get(os_key)

        if not config:
            Logger().warning(f"OS '{os_name}' not supported")
            return None

        return config

    def _get_parser(self, os_name: str, os_config: dict):
        parser_key = os_config.get("parser")

        if not parser_key:
            Logger().info(
                f"OS '{os_name}' has no package manager (scratch/distroless/minimal image)"
            )
            return None

        parser = PACKAGE_PARSERS.get(parser_key)
        if not parser:
            Logger().warning(f"No parser registered for '{parser_key}'")
            return None

        return parser

    def _scan_package_databases(
        self,
        filesystem_dir: Path,
        os_name: str,
        db_files: list[str],
        parser,
    ) -> list[dict]:
        packages: list[dict] = []
        found_any_db = False

        for db_file in db_files:
            db_path = filesystem_dir / db_file.lstrip("/")

            if not db_path.exists():
                Logger().debug(f"Package DB not found: {db_file}")
                continue

            found_any_db = True
            packages.extend(self._parse_db_file(db_path, parser))

        if not found_any_db:
            Logger().info(
                f"OS '{os_name}' detected but no package database files found"
            )

        return packages

    def _parse_db_file(self, db_path: Path, parser) -> list[dict]:
        try:
            with open(db_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            parsed = parser.parse(content)
            Logger().info(
                f"Parsed {len(parsed)} packages from {db_path}"
            )
            return parsed

        except Exception as e:
            Logger().error(f"Failed to parse {db_path}: {e}")
            return []
