"""
OS Package Configuration
Maps OS names to their package management systems and database locations.
"""

OS_PACKAGE_CONFIG = {
    # Debian-based systems (dpkg)
    "debian": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    "debian gnu/linux 12": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    "debian gnu/linux 11": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    "ubuntu": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    "ubuntu 22.04": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    "ubuntu 20.04": {
        "package_manager": "dpkg",
        "db_files": ["/var/lib/dpkg/status"],
        "parser": "dpkg",
        "mvp": True,
    },
    
    # Alpine Linux (apk)
    "alpine": {
        "package_manager": "apk",
        "db_files": ["/lib/apk/db/installed"],
        "parser": "apk",
        "mvp": True,
    },
    "alpine linux": {
        "package_manager": "apk",
        "db_files": ["/lib/apk/db/installed"],
        "parser": "apk",
        "mvp": True,
    },
    
    # Minimal/no package manager systems
    "scratch": {
        "package_manager": None,
        "db_files": [],
        "parser": None,
        "mvp": True,
    },
    "distroless": {
        "package_manager": None,
        "db_files": [],
        "parser": None,
        "mvp": True,
    },
    
    # RPM-based systems (parsing not implemented in MVP)
    "red hat enterprise linux": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "red hat enterprise linux 9": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "red hat enterprise linux 8": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "red hat enterprise linux 8.6": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "red hat enterprise linux 7": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "centos": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "centos linux 8": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "centos linux 7": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "fedora": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "almalinux": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "rocky linux": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "rocky": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    "oracle linux": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
    
    # Amazon Linux (RPM-based)
    "amazon linux": {
        "package_manager": "rpm",
        "db_files": ["/var/lib/rpm/Packages"],
        "parser": "rpm",  # Changed from None
        "mvp": True,
    },
}

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

