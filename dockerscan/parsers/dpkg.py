"""DPKG parser for Debian/Ubuntu systems."""


class DpkgParser:
    """Parse dpkg status database."""

    @staticmethod
    def parse(content: str) -> list[dict]:
        """
        Parse dpkg status file content.

        Args:
            content: Content of /var/lib/dpkg/status

        Returns:
            List of package dictionaries with 'name' and 'version' keys.
        """
        packages = []
        current_package = {}

        for line in content.split("\n"):
            line = line.rstrip()

            if not line:
                # Empty line marks end of package record
                if current_package.get("Package") and current_package.get("Version"):
                    packages.append({
                        "name": current_package["Package"],
                        "version": current_package["Version"],
                    })
                current_package = {}
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Capture relevant fields
            if key in ("Package", "Version"):
                current_package[key] = value

        # Don't forget the last package if file doesn't end with empty line
        if current_package.get("Package") and current_package.get("Version"):
            packages.append({
                "name": current_package["Package"],
                "version": current_package["Version"],
            })

        return packages

