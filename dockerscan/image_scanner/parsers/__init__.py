"""Package parsers registry for different OS package managers."""

from dockerscan.image_scanner.parsers.dpkg import DpkgParser
from dockerscan.image_scanner.parsers.apk import ApkParser
from dockerscan.image_scanner.parsers.rpm import RpmParser


PACKAGE_PARSERS = {
    "dpkg": DpkgParser(),
    "apk": ApkParser(),
    "rpm": RpmParser(),    #
}

