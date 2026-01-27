"""
Concrete OS configuration classes for specific operating systems.
Each OS version can have its own configuration with advisory support.
"""
from dockerscan.config.os_config_base import DebianBasedOS, RpmBasedOS, AlpineOS, MinimalOS


# ===== Debian Configurations =====

class DebianOS(DebianBasedOS):
    """Generic Debian configuration (fallback)"""

    def __init__(self, version: str = None):
        super().__init__("Debian GNU/Linux", version)


class Debian12(DebianBasedOS):
    """Debian 12 (Bookworm) with advisory support"""

    def __init__(self):
        super().__init__("Debian GNU/Linux", "12")

    @property
    def advisory_support(self) -> bool:
        return True

    @property
    def advisory_api(self) -> str:
        return "https://security-tracker.debian.org/tracker/data/json"

    @property
    def advisory_url_template(self) -> str:
        return "https://security-tracker.debian.org/tracker/{cve_id}"


class Debian11(DebianBasedOS):
    """Debian 11 (Bullseye) with advisory support"""

    def __init__(self):
        super().__init__("Debian GNU/Linux", "11")

    @property
    def advisory_support(self) -> bool:
        return True

    @property
    def advisory_api(self) -> str:
        return "https://security-tracker.debian.org/tracker/data/json"

    @property
    def advisory_url_template(self) -> str:
        return "https://security-tracker.debian.org/tracker/{cve_id}"


# ===== Ubuntu Configurations =====

class UbuntuOS(DebianBasedOS):
    """Generic Ubuntu configuration (fallback)"""

    def __init__(self, version: str = None):
        super().__init__("Ubuntu", version)


class Ubuntu2204(DebianBasedOS):
    """Ubuntu 22.04 (Jammy) with advisory support"""

    def __init__(self):
        super().__init__("Ubuntu", "22.04")

    @property
    def advisory_support(self) -> bool:
        return True

    @property
    def advisory_api(self) -> str:
        return "https://ubuntu.com/security/cves.json"

    @property
    def advisory_url_template(self) -> str:
        return "https://ubuntu.com/security/{cve_id}"


class Ubuntu2004(DebianBasedOS):
    """Ubuntu 20.04 (Focal) with advisory support"""

    def __init__(self):
        super().__init__("Ubuntu", "20.04")

    @property
    def advisory_support(self) -> bool:
        return True

    @property
    def advisory_api(self) -> str:
        return "https://ubuntu.com/security/cves.json"

    @property
    def advisory_url_template(self) -> str:
        return "https://ubuntu.com/security/{cve_id}"


# ===== Red Hat / CentOS Configurations =====

class RHELOS(RpmBasedOS):
    """Generic Red Hat Enterprise Linux configuration"""

    def __init__(self, version: str = None):
        super().__init__("Red Hat Enterprise Linux", version)


class RHEL9(RpmBasedOS):
    """Red Hat Enterprise Linux 9"""

    def __init__(self):
        super().__init__("Red Hat Enterprise Linux", "9")


class RHEL8(RpmBasedOS):
    """Red Hat Enterprise Linux 8"""

    def __init__(self):
        super().__init__("Red Hat Enterprise Linux", "8")


class RHEL86(RpmBasedOS):
    """Red Hat Enterprise Linux 8.6"""

    def __init__(self):
        super().__init__("Red Hat Enterprise Linux", "8.6")


class RHEL7(RpmBasedOS):
    """Red Hat Enterprise Linux 7"""

    def __init__(self):
        super().__init__("Red Hat Enterprise Linux", "7")


class CentOSOS(RpmBasedOS):
    """Generic CentOS configuration"""

    def __init__(self, version: str = None):
        super().__init__("CentOS", version)


class CentOS8(RpmBasedOS):
    """CentOS Linux 8"""

    def __init__(self):
        super().__init__("CentOS Linux", "8")


class CentOS7(RpmBasedOS):
    """CentOS Linux 7"""

    def __init__(self):
        super().__init__("CentOS Linux", "7")


# ===== Other RPM-based Systems =====

class FedoraOS(RpmBasedOS):
    """Fedora Linux"""

    def __init__(self, version: str = None):
        super().__init__("Fedora", version)


class AlmaLinuxOS(RpmBasedOS):
    """AlmaLinux"""

    def __init__(self, version: str = None):
        super().__init__("AlmaLinux", version)


class RockyLinuxOS(RpmBasedOS):
    """Rocky Linux"""

    def __init__(self, version: str = None):
        super().__init__("Rocky Linux", version)


class OracleLinuxOS(RpmBasedOS):
    """Oracle Linux"""

    def __init__(self, version: str = None):
        super().__init__("Oracle Linux", version)


class AmazonLinuxOS(RpmBasedOS):
    """Amazon Linux"""

    def __init__(self, version: str = None):
        super().__init__("Amazon Linux", version)


# ===== Alpine Configuration =====

class AlpineLinux(AlpineOS):
    """Alpine Linux"""

    def __init__(self, version: str = None):
        super().__init__("Alpine Linux", version)


# ===== Minimal OS Configurations =====

class ScratchOS(MinimalOS):
    """Scratch (minimal) container"""

    def __init__(self):
        super().__init__("scratch", None)


class DistrolessOS(MinimalOS):
    """Google Distroless container"""

    def __init__(self):
        super().__init__("distroless", None)

