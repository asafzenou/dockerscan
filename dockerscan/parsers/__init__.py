"""Package parsers registry for different OS package managers."""

from dockerscan.parsers.dpkg import DpkgParser
from dockerscan.parsers.apk import ApkParser


PACKAGE_PARSERS = {
    "dpkg": DpkgParser,
    "apk": ApkParser,
}

