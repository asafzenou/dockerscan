class DpkgParser:
    """Parse dpkg status database."""

    @staticmethod
    def parse(content: str) -> list[dict]:
        """Parse dpkg status file content."""
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

        if current_package.get("Package") and current_package.get("Version"):
            packages.append({
                "name": current_package["Package"],
                "version": current_package["Version"],
            })

        return packages

