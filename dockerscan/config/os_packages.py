OS_PACKAGE_CONFIG = {
    "debian": {
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
}
