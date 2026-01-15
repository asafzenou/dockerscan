"""Package parsers registry for different OS package managers."""

from dockerscan.parsers.dpkg import DpkgParser
from dockerscan.parsers.apk import ApkParser
from dockerscan.parsers.rpm import RpmParser


PACKAGE_PARSERS = {
    "dpkg": DpkgParser(),  # Instance, not class
    "apk": ApkParser(),    # Instance, not class
    "rpm": RpmParser(),    # Instance, not class
}

