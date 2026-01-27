"""
Base classes for OS configuration hierarchy.
Defines the structure for OS-specific package management and vulnerability scanning.
Architecture:
    OSConfig (ABC)
    ├── DebianBasedOS (Debian, Ubuntu)
    ├── RpmBasedOS (RHEL, CentOS, Fedora, etc.)
    ├── AlpineOS (Alpine Linux)
    └── MinimalOS (scratch, distroless)
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class OSConfig(ABC):
    """Abstract base class for operating system configuration."""

    def __init__(self, name: str, version: Optional[str] = None):
        self.name = name
        self.version = version

    @property
    @abstractmethod
    def package_manager(self) -> Optional[str]:
        """Package manager type (dpkg, rpm, apk, etc.)"""
        pass

    @property
    @abstractmethod
    def db_files(self) -> List[str]:
        """List of package database file paths"""
        pass

    @property
    @abstractmethod
    def parser(self) -> Optional[str]:
        """Parser name for extracting package information"""
        pass

    @property
    def mvp(self) -> bool:
        """Whether this OS is supported in MVP version"""
        return True

    @property
    def advisory_support(self) -> bool:
        """Whether advisory-based vulnerability matching is supported"""
        return False

    @property
    def advisory_api(self) -> Optional[str]:
        """API endpoint for OS security advisories"""
        return None

    @property
    def advisory_url_template(self) -> Optional[str]:
        """URL template for advisory links (use {cve_id} placeholder)"""
        return None

    def to_dict(self) -> Dict:
        """Convert configuration to dictionary format (backward compatibility)"""
        config = {
            "package_manager": self.package_manager,
            "db_files": self.db_files,
            "parser": self.parser,
            "mvp": self.mvp,
        }

        if self.advisory_support:
            config["advisory_support"] = self.advisory_support
            config["advisory_api"] = self.advisory_api
            config["advisory_url_template"] = self.advisory_url_template

        return config

    def __repr__(self) -> str:
        version_str = f" {self.version}" if self.version else ""
        return f"<{self.__class__.__name__}: {self.name}{version_str}>"


class DebianBasedOS(OSConfig):
    """Base class for Debian-based operating systems (Debian, Ubuntu)"""

    @property
    def package_manager(self) -> str:
        return "dpkg"

    @property
    def db_files(self) -> List[str]:
        return ["/var/lib/dpkg/status"]

    @property
    def parser(self) -> str:
        return "dpkg"


class RpmBasedOS(OSConfig):
    """Base class for RPM-based operating systems (RHEL, CentOS, Fedora, etc.)"""

    @property
    def package_manager(self) -> str:
        return "rpm"

    @property
    def db_files(self) -> List[str]:
        return ["/var/lib/rpm/Packages"]

    @property
    def parser(self) -> str:
        return "rpm"


class AlpineOS(OSConfig):
    """Alpine Linux configuration"""

    @property
    def package_manager(self) -> str:
        return "apk"

    @property
    def db_files(self) -> List[str]:
        return ["/lib/apk/db/installed"]

    @property
    def parser(self) -> str:
        return "apk"


class MinimalOS(OSConfig):
    """Base class for minimal OS images (scratch, distroless)"""

    @property
    def package_manager(self) -> Optional[str]:
        return None

    @property
    def db_files(self) -> List[str]:
        return []

    @property
    def parser(self) -> Optional[str]:
        return None

