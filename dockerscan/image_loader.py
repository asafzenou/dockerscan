"""Docker image save and extraction logic."""

import subprocess
import tarfile
from pathlib import Path
import tempfile
from dockerscan.logger import Logger



