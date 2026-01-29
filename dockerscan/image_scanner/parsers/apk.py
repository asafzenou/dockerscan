class ApkParser:
    """Parse APK (Alpine Package Keeper) database."""

    @staticmethod
    def parse(content: str) -> list[dict]:
        """Parse APK installed database content."""
        packages = []
        current_package = {}

        for line in content.split("\n"):
            line = line.rstrip()

            if not line:
                if current_package.get("name") and current_package.get("version"):
                    packages.append({
                        "name": current_package["name"],
                        "version": current_package["version"],
                    })
                current_package = {}
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "C":
                current_package["name"] = value
            elif key == "V":
                current_package["version"] = value

        if current_package.get("name") and current_package.get("version"):
            packages.append({
                "name": current_package["name"],
                "version": current_package["version"],
            })

        return packages

