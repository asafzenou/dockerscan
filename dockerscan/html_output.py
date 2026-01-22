"""HTML report generator for vulnerability scan results."""

from pathlib import Path
from datetime import datetime
from dockerscan.config.logger import Logger


def severity_class(severity: str) -> str:
    """Determine CSS class based on severity string."""
    if not severity:
        return "low"

    severity_upper = severity.upper()

    # Check for high severity indicators
    if "C:H" in severity_upper or "I:H" in severity_upper or "A:H" in severity_upper:
        return "high"

    # Check for medium severity indicators
    if "C:M" in severity_upper or "I:M" in severity_upper or "A:M" in severity_upper:
        return "medium"

    # Check for low severity indicators
    if "C:L" in severity_upper or "I:L" in severity_upper:
        return "medium"  # Consider low impact as medium for visibility

    return "low"


def generate_html_report(data: dict, output_dir: Path = None) -> Path:
    """
    Generate an HTML vulnerability report from scan data.

    Args:
        data: Dictionary containing 'os_info' and 'packages' with vulnerability data
        output_dir: Directory to save the report (default: html_reports/<timestamp>)

    Returns:
        Path to the generated HTML file
    """
    # Prepare output directory
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("html_reports") / timestamp

    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract data
    os_info = data.get("os_info", {})
    os_name = os_info.get("name", "Unknown OS")
    os_version = os_info.get("version", "")
    packages = data.get("packages", [])

    # Calculate statistics
    total_packages = len(packages)
    vulnerable_packages = sum(1 for pkg in packages if pkg.get("vulnerabilities", {}).get("count", 0) > 0)
    total_vulnerabilities = sum(pkg.get("vulnerabilities", {}).get("count", 0) for pkg in packages)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vulnerability Report - {os_name}</title>
<style>
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 20px;
}}
.container {{
    max-width: 1400px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}
h1 {{
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}}
h2 {{
    color: #34495e;
    margin-top: 30px;
}}
.summary {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}}
.summary-card {{
    background: #ecf0f1;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}}
.summary-card h3 {{
    margin: 0 0 10px 0;
    color: #7f8c8d;
    font-size: 14px;
    text-transform: uppercase;
}}
.summary-card .value {{
    font-size: 32px;
    font-weight: bold;
    color: #2c3e50;
}}
.os-info {{
    background: #e8f4f8;
    padding: 15px;
    border-radius: 6px;
    border-left: 4px solid #3498db;
    margin: 20px 0;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}}
th {{
    background: #34495e;
    color: white;
    font-weight: 600;
}}
tr.vulnerable {{
    background-color: #fdecea;
}}
tr:hover {{
    background-color: #f8f9fa;
}}
tr.vulnerable:hover {{
    background-color: #fce4e1;
}}
.badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 4px;
    color: white;
    font-size: 11px;
    font-weight: bold;
    margin: 2px 0;
}}
.high {{
    background: #c0392b;
}}
.medium {{
    background: #f39c12;
}}
.low {{
    background: #27ae60;
}}
.vuln-details {{
    font-size: 13px;
    line-height: 1.6;
}}
.vuln-item {{
    margin-bottom: 12px;
    padding: 8px;
    background: #f9f9f9;
    border-radius: 4px;
}}
a {{
    color: #2980b9;
    text-decoration: none;
}}
a:hover {{
    text-decoration: underline;
}}
.timestamp {{
    color: #7f8c8d;
    font-size: 14px;
    margin-top: 30px;
    text-align: right;
}}
</style>
</head>
<body>
<div class="container">

<h1>🔒 Security Vulnerability Report</h1>

<div class="summary">
    <div class="summary-card">
        <h3>Total Packages</h3>
        <div class="value">{total_packages}</div>
    </div>
    <div class="summary-card">
        <h3>Vulnerable Packages</h3>
        <div class="value" style="color: #e74c3c;">{vulnerable_packages}</div>
    </div>
    <div class="summary-card">
        <h3>Total Vulnerabilities</h3>
        <div class="value" style="color: #c0392b;">{total_vulnerabilities}</div>
    </div>
</div>

<h2>Operating System</h2>
<div class="os-info">
    <strong>{os_name}</strong>
    {f'<span style="color: #7f8c8d;"> – Version {os_version}</span>' if os_version else ''}
</div>

<h2>Package Vulnerabilities</h2>
<table>
<thead>
<tr>
    <th>Package</th>
    <th>Version</th>
    <th>Vulnerabilities</th>
    <th>Details</th>
</tr>
</thead>
<tbody>
"""

    # Generate table rows
    for pkg in packages:
        pkg_name = pkg.get("name", "unknown")
        pkg_version = pkg.get("version", "unknown")
        vulnerabilities = pkg.get("vulnerabilities", {})
        vuln_count = vulnerabilities.get("count", 0)
        vuln_items = vulnerabilities.get("items", [])

        row_class = "vulnerable" if vuln_count > 0 else ""

        # Build vulnerability details
        if vuln_count > 0:
            details_html = ""
            for vuln in vuln_items:
                vuln_id = vuln.get("id", "UNKNOWN")
                vuln_summary = vuln.get("summary", "No summary available")
                vuln_severity = vuln.get("severity", "Unknown")
                vuln_url = vuln.get("details_url", "#")

                sev_class = severity_class(vuln_severity)

                details_html += f"""
                <div class="vuln-item">
                    <span class="badge {sev_class}">{vuln_id}</span><br>
                    <small style="color: #555;">{vuln_summary}</small><br>
                    <small style="color: #7f8c8d;"><strong>Severity:</strong> {vuln_severity}</small><br>
                    <a href="{vuln_url}" target="_blank">🔗 View details</a>
                </div>
                """
        else:
            details_html = '<span style="color: #27ae60;">✓ No known vulnerabilities</span>'

        html += f"""
<tr class="{row_class}">
    <td><strong>{pkg_name}</strong></td>
    <td><code>{pkg_version}</code></td>
    <td style="text-align: center;"><strong>{vuln_count}</strong></td>
    <td class="vuln-details">{details_html}</td>
</tr>
"""

    html += f"""
</tbody>
</table>

<div class="timestamp">
    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</div>

</div>
</body>
</html>
"""

    # Write HTML file
    output_file = output_dir / "vulnerability_report.html"
    output_file.write_text(html, encoding="utf-8")

    Logger().info(f"HTML report generated: {output_file.resolve()}")

    return output_file

