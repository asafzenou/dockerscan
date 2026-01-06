OS_PACKAGE_CONFIG = {
    "debian gnu/linux 12": {
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
    "alpine": {
        "package_manager": "apk",
        "db_files": ["/lib/apk/db/installed"],
        "parser": "apk",
        "mvp": True,
    },
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
    "red hat enterprise linux 8.6": {
        "package_manager": "rpm",
        "db_files": ["var/lib/rpm"],
        "parser": "rpm",
    }
}

RELEVANT_PATHS = (
    "etc/os-release",
    "usr/lib/os-release",
    "var/lib/dpkg/status",
    "lib/apk/db/installed",
    "var/lib/rpm",
    "usr/lib/sysimage/rpm",
)

