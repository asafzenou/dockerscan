"""Configuration module for OS-specific package management and vulnerability scanning."""

# Base classes
from dockerscan.config.os_config_base import (
    OSConfig,
    DebianBasedOS,
    RpmBasedOS,
    AlpineOS,
    MinimalOS,
)

# Concrete OS configurations
from dockerscan.config.os_configs import (
    # Debian
    DebianOS,
    Debian12,
    Debian11,
    # Ubuntu
    UbuntuOS,
    Ubuntu2204,
    Ubuntu2004,
    # RHEL/CentOS
    RHELOS,
    RHEL9,
    RHEL8,
    RHEL86,
    RHEL7,
    CentOSOS,
    CentOS8,
    CentOS7,
    # Other RPM
    FedoraOS,
    AlmaLinuxOS,
    RockyLinuxOS,
    OracleLinuxOS,
    AmazonLinuxOS,
    # Alpine
    AlpineLinux,
    # Minimal
    ScratchOS,
    DistrolessOS,
)

# Registry and helper functions
from dockerscan.config.os_packages import (
    OS_PACKAGE_CONFIG,
    RELEVANT_PATHS,
    get_os_config,
    get_os_config_dict,
    list_supported_os,
    list_advisory_supported_os,
)

# Logger
from dockerscan.config.logger import Logger

__all__ = [
    # Base classes
    "OSConfig",
    "DebianBasedOS",
    "RpmBasedOS",
    "AlpineOS",
    "MinimalOS",
    # Concrete OS configs
    "DebianOS",
    "Debian12",
    "Debian11",
    "UbuntuOS",
    "Ubuntu2204",
    "Ubuntu2004",
    "RHELOS",
    "RHEL9",
    "RHEL8",
    "RHEL86",
    "RHEL7",
    "CentOSOS",
    "CentOS8",
    "CentOS7",
    "FedoraOS",
    "AlmaLinuxOS",
    "RockyLinuxOS",
    "OracleLinuxOS",
    "AmazonLinuxOS",
    "AlpineLinux",
    "ScratchOS",
    "DistrolessOS",
    # Registry and helpers
    "OS_PACKAGE_CONFIG",
    "RELEVANT_PATHS",
    "get_os_config",
    "get_os_config_dict",
    "list_supported_os",
    "list_advisory_supported_os",
    # Logger
    "Logger",
]

