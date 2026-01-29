# dockerscan

A comprehensive Docker image scanner that detects OS information, scans packages, identifies vulnerabilities, and generates detailed reports.

## Installation

```bash
pip install -e .
```

## Usage

```bash
dockerscan scan <image_name>
```

Example:
```bash
dockerscan scan ubuntu:20.04
```

## Output

After scanning completes, dockerscan generates a comprehensive **HTML vulnerability report** that is automatically opened in your default browser. The report includes:

- **Summary Dashboard** - Total packages, vulnerable packages, and vulnerability count
- **OS Information** - Detected operating system and version
- **Runtime Configuration** - Container entrypoint, command, user, and exposed ports
- **Package Vulnerabilities Table** with:
  - Package name and version
  - Vulnerability count
  - Risk analysis and severity badges
  - CVE details with CVSS scores
  - Patch status and fix information
  - References and upstream data
- **Interactive Filtering** - Filter by package name or vulnerability count
- **Timestamp** - Report generation date and time

The HTML reports are saved in: `html_reports/<OS_Name>_<Version>_<Timestamp>/vulnerability_report.html`

### Example Report Preview

Here's what the vulnerability report looks like in your browser:

<iframe style="width: 100%; height: 600px; border: 2px solid #3498db; border-radius: 8px; margin: 20px 0;" srcdoc="
<!DOCTYPE html>
<html>
<head>
<style>
body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    background: #1a1a1a; 
    margin: 0; 
    padding: 20px;
    color: #e0e0e0;
}
.container { 
    max-width: 100%; 
    background: #2d2d2d; 
    padding: 20px; 
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.5);
}
h1 { 
    color: #64b5f6; 
    border-bottom: 3px solid #3498db; 
    padding-bottom: 10px; 
    font-size: 24px; 
}
h2 { 
    color: #90caf9; 
    margin: 20px 0 10px 0; 
    font-size: 16px; 
}
.summary { 
    display: grid; 
    grid-template-columns: repeat(3, 1fr); 
    gap: 15px; 
    margin: 20px 0; 
}
.summary-card { 
    background: #3a3a3a; 
    padding: 15px; 
    border-radius: 8px; 
    border-left: 4px solid #3498db; 
    text-align: center; 
}
.summary-card h3 { 
    margin: 0 0 10px 0; 
    color: #64b5f6; 
    font-size: 12px; 
    text-transform: uppercase; 
}
.summary-card .value { 
    font-size: 28px; 
    font-weight: bold; 
    color: #90caf9; 
}
.os-info { 
    background: #1e3a5f; 
    padding: 15px; 
    border-radius: 6px; 
    border-left: 4px solid #3498db; 
    margin: 15px 0; 
    font-size: 14px; 
    color: #b3e5fc;
}
table { 
    width: 100%; 
    border-collapse: collapse; 
    margin-top: 15px; 
    font-size: 12px;
    background: #3a3a3a;
}
th { 
    background: #1a1a1a; 
    color: #64b5f6; 
    font-weight: 600;
    padding: 8px;
    border: 1px solid #444;
}
td { 
    border: 1px solid #444; 
    padding: 8px; 
    text-align: left; 
    color: #e0e0e0;
}
tr.vulnerable { 
    background-color: #4a1a1a; 
}
tr.vulnerable:hover {
    background-color: #5a2a2a;
}
tr:hover {
    background-color: #3f3f3f;
}
.badge { 
    display: inline-block; 
    padding: 3px 8px; 
    border-radius: 4px; 
    color: white; 
    font-size: 10px; 
    font-weight: bold; 
    background: #c0392b; 
}
.patch-status { 
    display: inline-block; 
    padding: 3px 6px; 
    border-radius: 3px; 
    font-size: 10px; 
    font-weight: bold; 
    margin-top: 4px; 
}
.patch-available { 
    background: #1b5e20; 
    color: #81c784; 
    border: 1px solid #2e7d32; 
}
.patch-not-available {
    background: #b71c1c;
    color: #ef9a9a;
    border: 1px solid #d32f2f;
}
.fixed-version { 
    font-family: 'Courier New', monospace; 
    background: #1a1a1a; 
    padding: 2px 6px; 
    border-radius: 3px; 
    font-size: 12px;
    color: #81c784;
}
.timestamp { 
    color: #90a4ae; 
    font-size: 12px; 
    margin-top: 15px; 
    text-align: right; 
}
a {
    color: #64b5f6;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
small {
    color: #b0bec5;
}
code {
    background: #1a1a1a;
    color: #81c784;
    padding: 2px 4px;
    border-radius: 3px;
}
</style>
</head>
<body>
<div class='container'>
<h1>🔒 Security Vulnerability Report</h1>
<div class='summary'>
<div class='summary-card'><h3>Total Packages</h3><div class='value'>5</div></div>
<div class='summary-card'><h3>Vulnerable Packages</h3><div class='value' style='color: #ef5350;'>2</div></div>
<div class='summary-card'><h3>Total Vulnerabilities</h3><div class='value' style='color: #ef5350;'>2</div></div>
</div>
<h2>Operating System</h2>
<div class='os-info'><strong>Debian GNU/Linux</strong> – Version 12</div>
<h2>Package Vulnerabilities</h2>
<table>
<thead><tr><th>Package</th><th>Version</th><th>Vulns</th><th>Status</th></tr></thead>
<tbody>
<tr class='vulnerable'>
<td><strong>bash</strong><br><small>🔴 Runtime</small></td>
<td><code>5.2.15-2+b7</code></td>
<td style='text-align: center;'><strong>1</strong></td>
<td><span class='badge'>CVE-2022-3715</span><br><span class='patch-status patch-available'>✓ Patched</span></td>
</tr>
<tr class='vulnerable'>
<td><strong>apt</strong><br><small>⚪ Build Time</small></td>
<td><code>2.6.1</code></td>
<td style='text-align: center;'><strong>1</strong></td>
<td><span class='badge'>CVE-2011-3374</span><br><span class='patch-status patch-not-available'>✗ No Patch</span></td>
</tr>
<tr>
<td><strong>autoconf</strong><br><small>⚪ Build Time</small></td>
<td><code>2.71-3</code></td>
<td style='text-align: center;'><strong>0</strong></td>
<td><span style='color: #81c784;'>✓ Clean</span></td>
</tr>
<tr>
<td><strong>automake</strong><br><small>⚪ Build Time</small></td>
<td><code>1:1.16.5-1.3</code></td>
<td style='text-align: center;'><strong>0</strong></td>
<td><span style='color: #81c784;'>✓ Clean</span></td>
</tr>
<tr>
<td><strong>autotools-dev</strong><br><small>⚪ Build Time</small></td>
<td><code>20220109.1</code></td>
<td style='text-align: center;'><strong>0</strong></td>
<td><span style='color: #81c784;'>✓ Clean</span></td>
</tr>
</tbody>
</table>
<div class='timestamp'>Generated: 2026-01-29 22:51:16</div>
</div>
</body>
</html>
"></iframe>

## What it does

1. Saves the Docker image using `docker save`
2. Extracts the image tar archive
3. Reconstructs the merged filesystem from Docker layers
4. Reads `/etc/os-release` from the filesystem
5. Prints the detected OS name and version

## Example Output

```
Scanning Docker image: ubuntu:20.04
Extracting image to temporary directory...
  Running: docker save ubuntu:20.04
  Extracting tar archive...
Reconstructing filesystem from layers...
  Found 3 layers
Detecting OS...
Detected OS: Ubuntu 20.04.6 LTS
```

## Requirements

- Python 3.11+
- Docker installed and running
- The Docker image must exist locally or be pullable

## Technologies & APIs

### Core Technologies

- **Python 3.11+** - Primary programming language
- **Docker API** - For saving and managing Docker images
- **requests** - HTTP library for API calls

### External APIs & Services

- **OSV.dev API** (`https://api.osv.dev/v1/query`) - Open Source Vulnerability database for querying known vulnerabilities in packages
  - Supports multiple ecosystems: Debian, Alpine, Red Hat
  - Provides detailed CVE information and patch status

### Project Architecture

**Key Components:**

1. **Image Scanner** (`dockerscan/image_scanner/`)
   - Extracts Docker images and reconstructs filesystem layers
   - Detects OS information from `/etc/os-release`
   - Scans for installed packages using OS-specific parsers

2. **Package Parsers** (`dockerscan/image_scanner/parsers/`)
   - `dpkg.py` - Debian/Ubuntu package parsing
   - `rpm.py` - RedHat/CentOS/Fedora package parsing
   - `apk.py` - Alpine Linux package parsing

3. **Vulnerability Enrichment** (`dockerscan/data_packagers_checker/`)
   - Queries OSV.dev API for each detected package
   - Enriches packages with vulnerability data
   - Provides risk assessment and recommendations

4. **Reports** (`dockerscan/reports/`)
   - Generates HTML vulnerability reports
   - Includes severity classification (High, Medium, Low)
   - Provides actionable recommendations

5. **Configuration System** (`dockerscan/config/`)
   - Modular OS configuration support
   - Extensible package manager definitions
   - Centralized logging

## Adding Support for New Linux Operating Systems

This guide explains how to add support for a new Linux distribution to dockerscan.

### Overview of the Architecture

The dockerscan project detects OS information and scans packages from Docker images. The OS detection system is modular and extensible:

- **OS Configurations** (`dockerscan/config/`) - Define OS metadata and detection methods
- **Package Parsers** (`dockerscan/image_scanner/parsers/`) - Extract packages from OS-specific formats
- **OS Detector** (`dockerscan/image_scanner/os_detector.py`) - Identifies the OS from image filesystem

### Step-by-Step Guide

#### Step 1: Create OS Configuration File

Create a new file in `dockerscan/config/` for your OS. Example for Fedora:

**File**: `dockerscan/config/os_fedora.py`

```python
from dockerscan.config.os_config_base import OSConfigBase

class FedoraConfig(OSConfigBase):
    def __init__(self):
        super().__init__(
            os_name="Fedora",
            os_version="39",
            package_manager="dnf",
            detection_files=["/etc/os-release", "/etc/fedora-release"]
        )
```

**Parameters:**
- `os_name`: Human-readable OS name
- `os_version`: Default version (can be overridden by detection)
- `package_manager`: Package manager type (dnf, apt, apk, yum, etc.)
- `detection_files`: List of files to check for OS identification

#### Step 2: Register OS in Configuration Registry

Update `dockerscan/config/os_configs.py` to register your new OS:

```python
from dockerscan.config.os_fedora import FedoraConfig

OS_CONFIGS = {
    "debian": DebianConfig(),
    "ubuntu": UbuntuConfig(),
    "alpine": AlpineConfig(),
    "rhel": RHELConfig(),
    "fedora": FedoraConfig(),  # Add this line
}
```

#### Step 3: Create or Reuse Package Parser

Package parsers extract installed packages from OS-specific formats.

**If your OS uses an existing package manager format**, reuse the parser:
- **apt-based systems** (Ubuntu, Debian) → Use `dockerscan/image_scanner/parsers/dpkg.py`
- **rpm-based systems** (RHEL, CentOS, Fedora) → Use `dockerscan/image_scanner/parsers/rpm.py`
- **apk-based systems** (Alpine) → Use `dockerscan/image_scanner/parsers/apk.py`

**If your OS uses a unique package format**, create a new parser:

**File**: `dockerscan/image_scanner/parsers/myos.py`

```python
class MyOSPackageParser:
    @staticmethod
    def parse(filesystem_dir):
        """
        Parse packages from the filesystem.
        
        Args:
            filesystem_dir: Path to the extracted filesystem
            
        Returns:
            List of dicts with 'name' and 'version' keys
        """
        packages = []
        # Your custom parsing logic here
        return packages
```

#### Step 4: Update Package Configuration (Optional)

If your OS has specific package metadata, update `dockerscan/config/os_packages.py`:

```python
OS_PACKAGE_CONFIGS = {
    "fedora": {
        "package_manager": "dnf",
        "parser": "rpm",
        "special_packages": [],
    },
}
```

#### Step 5: Verify OS Detection

Check that `dockerscan/image_scanner/os_detector.py` correctly identifies your OS by reading `/etc/os-release`:

```python
def detect_os_from_release_file(filesystem_dir):
    """Reads /etc/os-release to identify OS"""
    # Should automatically detect your OS if it follows standard format
```

Most modern Linux distributions follow the `/etc/os-release` standard, so no changes needed.

### File Checklist

- [ ] Created `dockerscan/config/os_myos.py` with OS configuration
- [ ] Registered OS in `dockerscan/config/os_configs.py`
- [ ] Created or identified appropriate parser in `dockerscan/image_scanner/parsers/`
- [ ] (Optional) Updated `dockerscan/config/os_packages.py` with OS-specific metadata
- [ ] Verified OS detection in `dockerscan/image_scanner/os_detector.py`

### Example: Adding Ubuntu 24.04 Support

1. **Create config** (`dockerscan/config/os_ubuntu.py`):
```python
from dockerscan.config.os_config_base import OSConfigBase

class UbuntuConfig(OSConfigBase):
    def __init__(self):
        super().__init__(
            os_name="Ubuntu",
            os_version="24.04",
            package_manager="apt",
            detection_files=["/etc/os-release", "/etc/lsb-release"]
        )
```

2. **Register** in `dockerscan/config/os_configs.py`:
```python
"ubuntu": UbuntuConfig(),
```

3. **Use existing parser**: Reuse `dockerscan/image_scanner/parsers/dpkg.py`

4. **Done!** The scanner now supports Ubuntu 24.04

### Supported Operating Systems

- Alpine Linux
- Debian GNU/Linux
- Red Hat Enterprise Linux (RHEL)
- Ubuntu (via dpkg/Debian parser)

### Troubleshooting

**Q: My OS is not being detected**
- Ensure the OS follows the `/etc/os-release` standard
- Add detection files to your OS config's `detection_files` parameter

**Q: Packages are not being parsed**
- Verify the correct parser is registered for your OS's package manager
- Check that the parser can access the package database location in the extracted filesystem

**Q: I see errors about missing package files**
- Some OSes store packages differently (e.g., in squashfs format)
- Create a custom parser that handles your OS's specific format
