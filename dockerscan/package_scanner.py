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

        Logger().info(f"Using config for '{os_name}': package_manager={os_config.get('package_manager')}, parser={os_config.get('parser')}")
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
                        f"{package_manager.upper()} database detected at {os_config.get('db_files')} but parsing not implemented (MVP limitation)"
                    )
                    return {
                        "packages": [],
                        "note": f"{package_manager.upper()} database detected but parsing not implemented",
                        "package_manager": package_manager
                    }
                else:
                    Logger().warning(f"OS '{os_name}' uses {package_manager} but database not found at {os_config.get('db_files')}")
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
            Logger().debug(f"Checking for package database: {db_file} -> {db_path}")
            if db_path.exists():
                Logger().debug(f"Found package database: {db_path}")
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
            Logger().debug(f"No parser configured for OS '{os_name}' (intentional: MVP limitation or minimal image)")
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
            # Check if parser needs the file path (RPM) or content (dpkg/apk)
            if hasattr(parser, 'parse_file'):
                # Parser has parse_file method (for binary files like RPM)
                parsed = parser.parse_file(db_path)
            else:
                # Parser expects content string (for text files like dpkg/apk)
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
