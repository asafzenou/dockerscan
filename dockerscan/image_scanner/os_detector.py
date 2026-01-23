"""OS detection from /etc/os-release."""

from pathlib import Path

class OSDetection:
    version_dict = {}

    @staticmethod
    def detect_os(filesystem_dir: Path) -> dict[str, str]:
        """Detect OS name and version from /etc/os-release."""
        os_release_path = filesystem_dir / "etc" / "os-release"

        if not os_release_path.exists():
            return None

        os_info = {}
        with open(os_release_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip('"\'')
                    os_info[key] = value

        name = os_info.get('NAME') or os_info.get('ID', 'unknown')
        version = os_info.get('VERSION_ID') or os_info.get('VERSION', '')

        name = name.strip('"\'')
        version = version.strip('"\'')
        os_info['name'] = name
        os_info['version'] = version
        OSDetection.version_dict = os_info
        if version:
            return {'name': name, 'version': version}
        else:
            return {'name': name}

    @staticmethod
    def get_os():
        try:
            if not OSDetection.version_dict:
                return "dont have name and version info"

            name = OSDetection.version_dict.get('name')
            version = OSDetection.version_dict.get('version')

            if not name:
                return "dont have name info"
            if not version:
                return name

            return f"{name} {version}"
        except Exception:
            return "dont have name and version info"

