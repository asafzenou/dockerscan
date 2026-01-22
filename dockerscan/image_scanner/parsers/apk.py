"""APK parser for Alpine systems."""


class ApkParser:
    """Parse APK (Alpine Package Keeper) database."""

    @staticmethod
    def parse(content: str) -> list[dict]:
        """
        Parse APK installed database content.

        Args:
            content: Content of /lib/apk/db/installed

        Returns:
            List of package dictionaries with 'name' and 'version' keys.
        """
        packages = []
        current_package = {}

        for line in content.split("\n"):
            line = line.rstrip()

            if not line:
                # Empty line marks end of package record
                if current_package.get("name") and current_package.get("version"):
                    packages.append({
                        "name": current_package["name"],
                        "version": current_package["version"],
                    })
                current_package = {}
                continue

            # APK format: key:value
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # APK uses different field names: "C" for package name, "V" for version
            if key == "C":
                current_package["name"] = value
            elif key == "V":
                current_package["version"] = value

        # Don't forget the last package if file doesn't end with empty line
        if current_package.get("name") and current_package.get("version"):
            packages.append({
                "name": current_package["name"],
                "version": current_package["version"],
            })

        return packages

