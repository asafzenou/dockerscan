"""
OS Package Configuration
Object-oriented registry for OS-specific configurations.
Each OS has its own class with package management and advisory support.
"""
from dockerscan.config.os_configs import (
    # Debian
    DebianOS, Debian12, Debian11,
    # Ubuntu
    UbuntuOS, Ubuntu2204, Ubuntu2004,
    # RHEL/CentOS
    RHELOS, RHEL9, RHEL8, RHEL86, RHEL7,
    CentOSOS, CentOS8, CentOS7,
    # Other RPM-based
    FedoraOS, AlmaLinuxOS, RockyLinuxOS, OracleLinuxOS, AmazonLinuxOS,
    # Alpine
    AlpineLinux,
    # Minimal
    ScratchOS, DistrolessOS
)


# Registry mapping OS name strings to configuration objects
_OS_REGISTRY = {
    # Debian-based systems
    "debian": DebianOS(),
    "debian gnu/linux": DebianOS(),
    "debian gnu/linux 12": Debian12(),
    "debian gnu/linux 11": Debian11(),

    # Ubuntu
    "ubuntu": UbuntuOS(),
    "ubuntu 22.04": Ubuntu2204(),
    "ubuntu 20.04": Ubuntu2004(),

    # Alpine
    "alpine": AlpineLinux(),
    "alpine linux": AlpineLinux(),

    # Minimal systems
    "scratch": ScratchOS(),
    "distroless": DistrolessOS(),

    # Red Hat Enterprise Linux
    "red hat enterprise linux": RHELOS(),
    "red hat enterprise linux 9": RHEL9(),
    "red hat enterprise linux 8": RHEL8(),
    "red hat enterprise linux 8.6": RHEL86(),
    "red hat enterprise linux 7": RHEL7(),

    # CentOS
    "centos": CentOSOS(),
    "centos linux": CentOSOS(),
    "centos linux 8": CentOS8(),
    "centos linux 7": CentOS7(),

    # Other RPM-based systems
    "fedora": FedoraOS(),
    "almalinux": AlmaLinuxOS(),
    "rocky linux": RockyLinuxOS(),
    "rocky": RockyLinuxOS(),
    "oracle linux": OracleLinuxOS(),
    "amazon linux": AmazonLinuxOS(),
}


# Backward compatibility: provide dictionary-like access
OS_PACKAGE_CONFIG = {
    key: config.to_dict()
    for key, config in _OS_REGISTRY.items()
}


def get_os_config(os_name: str, os_version: str = None):
    """
    Get OS configuration object for the given OS name and version.

    Args:
        os_name: OS name (e.g., "Debian GNU/Linux", "Ubuntu")
        os_version: Optional OS version (e.g., "12", "22.04")

    Returns:
        OSConfig object or None if not found

    Example:
        >>> config = get_os_config("Debian GNU/Linux", "12")
        >>> config.advisory_support
        True
    """
    # Try exact match with version
    if os_version:
        key = f"{os_name.lower()} {os_version}".strip()
        if key in _OS_REGISTRY:
            return _OS_REGISTRY[key]

    # Try without version
    key = os_name.lower().strip()
    if key in _OS_REGISTRY:
        return _OS_REGISTRY[key]

    return None


def get_os_config_dict(os_name: str, os_version: str = None) -> dict:
    """
    Get OS configuration as dictionary (backward compatibility).

    Args:
        os_name: OS name
        os_version: Optional OS version

    Returns:
        Configuration dictionary or None
    """
    config = get_os_config(os_name, os_version)
    return config.to_dict() if config else None


def list_supported_os() -> list:
    """Get list of all supported OS configurations."""
    return list(_OS_REGISTRY.keys())


def list_advisory_supported_os() -> list:
    """Get list of OS configurations with advisory support."""
    return [
        key for key, config in _OS_REGISTRY.items()
        if config.advisory_support
    ]


# Paths to extract from Docker images for OS detection and package scanning
RELEVANT_PATHS = (
    # OS detection files
    "etc/os-release",
    "usr/lib/os-release",
    # Package database files
    "var/lib/dpkg/status",          # Debian/Ubuntu
    "lib/apk/db/installed",         # Alpine
    "var/lib/rpm/Packages",         # RPM-based (RHEL, CentOS, Fedora, etc.)
    "usr/lib/sysimage/rpm/Packages", # Modern RPM location
)


# Paths to extract from Docker images for OS detection and package scanning
RELEVANT_PATHS = (
    # OS detection files
    "etc/os-release",
    "usr/lib/os-release",
    # Package database files
    "var/lib/dpkg/status",          # Debian/Ubuntu
    "lib/apk/db/installed",         # Alpine
    "var/lib/rpm/Packages",         # RPM-based (RHEL, CentOS, Fedora, etc.)
    "usr/lib/sysimage/rpm/Packages", # Modern RPM location
)

