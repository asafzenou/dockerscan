from pathlib import Path
from dockerscan.config.os_packages import OS_PACKAGE_CONFIG
from dockerscan.parsers import PACKAGE_PARSERS
from dockerscan.logger import Logger


class PackageScanner:
    """Scan and extract OS packages from a Docker image filesystem."""

    def scan(self, filesystem_dir: Path, os_name: str) -> dict:
        """
        Scan for packages in the filesystem.

        Returns:
            dict with 'packages' list and optional 'note' explaining limitations
        """
        os_config = self._get_os_config(os_name)
        if not os_config:
            return {"packages": []}

        parser = self._get_parser(os_name, os_config)

        # No parser available
        if not parser:
            # Check if this is a known package manager with intentionally skipped parsing (MVP)
            package_manager = os_config.get("package_manager")
            if package_manager:
                # Check if database actually exists
                db_detected = self._check_package_databases_exist(
                    filesystem_dir, os_config.get("db_files", [])
                )
                if db_detected:
                    Logger().info(
                        f"RPM database detected but parsing not implemented (MVP limitation)"
                    )
                    return {
                        "packages": [],
                        "note": f"{package_manager.upper()} database detected but parsing not implemented"
                    }
                else:
                    Logger().info(f"OS '{os_name}' detected but no package database found")
            else:
                # No package manager at all (scratch, distroless)
                Logger().info(
                    f"OS '{os_name}' has no package manager (scratch/distroless/minimal image)"
                )
            return {"packages": []}

        # Parser available - scan packages
        packages = self._scan_package_databases(
            filesystem_dir,
            os_name,
            os_config["db_files"],
            parser,
        )
        return {"packages": packages}

    # ───────────────────────── helpers ─────────────────────────

    def _check_package_databases_exist(self, filesystem_dir: Path, db_files: list[str]) -> bool:
        """Check if any package database files exist in the filesystem."""
        for db_file in db_files:
            db_path = filesystem_dir / db_file.lstrip("/")
            if db_path.exists():
                return True
        return False

    def _get_os_config(self, os_name: str) -> dict | None:
        os_key = os_name.lower()
        config = OS_PACKAGE_CONFIG.get(os_key)

        if not config:
            Logger().warning(f"OS '{os_name}' not supported")
            return None

        return config

    def _get_parser(self, os_name: str, os_config: dict):
        parser_key = os_config.get("parser")

        # No parser configured (intentional: scratch/distroless or MVP limitation)
        if parser_key is None:
            return None

        # Parser key exists but no implementation (unexpected)
        parser = PACKAGE_PARSERS.get(parser_key)
        if not parser:
            Logger().warning(f"Parser '{parser_key}' not registered (implementation missing)")
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
