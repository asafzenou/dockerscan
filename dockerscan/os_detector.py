"""OS detection from /etc/os-release."""

from pathlib import Path


def detect_os(filesystem_dir: Path) -> str:
    """
    Detect OS name and version from /etc/os-release.
    
    Args:
        filesystem_dir: Root of the reconstructed filesystem
        
    Returns:
        String with OS name and version (e.g., "ubuntu 20.04")
    """
    os_release_path = filesystem_dir / "etc" / "os-release"
    
    if not os_release_path.exists():
        return None
    
    # Parse os-release file
    os_info = {}
    with open(os_release_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                # Remove quotes from value
                value = value.strip('"\'')
                os_info[key] = value
    
    # Extract OS name and version
    name = os_info.get("NAME") or os_info.get("ID", "unknown")
    version = os_info.get("VERSION_ID") or os_info.get("VERSION", "")
    
    # Clean up name (remove quotes if any)
    name = name.strip('"\'')
    version = version.strip('"\'')
    
    if version:
        return f"{name} {version}"
    else:
        return name

