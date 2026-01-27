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
    runtime_context = data.get("runtime_context", {})

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
.patch-status {{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: bold;
    margin-top: 6px;
}}
.patch-available {{
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}}
.patch-not-available {{
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}}
.fixed-version {{
    font-family: 'Courier New', monospace;
    background: #e9ecef;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
}}
.vuln-meta {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 8px;
    margin-top: 8px;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    font-size: 12px;
}}
.meta-item {{
    display: flex;
    flex-direction: column;
}}
.meta-label {{
    font-weight: bold;
    color: #34495e;
    font-size: 11px;
    text-transform: uppercase;
}}
.meta-value {{
    color: #555;
    word-break: break-word;
}}
.urgency-critical {{
    background: #c0392b;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
}}
.urgency-high {{
    background: #e74c3c;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
}}
.urgency-medium {{
    background: #f39c12;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
}}
.urgency-low {{
    background: #27ae60;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
}}
.references-list {{
    margin-top: 6px;
    padding-left: 16px;
}}
.references-list li {{
    margin: 3px 0;
    font-size: 11px;
}}
.references-list a {{
    color: #2980b9;
    text-decoration: none;
}}
.references-list a:hover {{
    text-decoration: underline;
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
.filters {{
    background: #ecf0f1;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}}
.filter-group {{
    display: inline-block;
    margin-right: 20px;
    margin-bottom: 10px;
}}
.filter-group label {{
    display: block;
    font-weight: bold;
    color: #34495e;
    margin-bottom: 5px;
    font-size: 14px;
}}
.filter-group input,
.filter-group select {{
    padding: 8px 12px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-size: 14px;
    min-width: 200px;
}}
.filter-group button {{
    padding: 8px 16px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    margin-top: 21px;
}}
.filter-group button:hover {{
    background: #2980b9;
}}
.no-results {{
    text-align: center;
    padding: 40px;
    color: #7f8c8d;
    font-size: 16px;
}}
.runtime-context {{
    background: #f0f8ff;
    padding: 20px;
    border-radius: 6px;
    border-left: 4px solid #2980b9;
    margin: 20px 0;
}}
.runtime-context h3 {{
    margin: 0 0 15px 0;
    color: #34495e;
    font-size: 16px;
}}
.runtime-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}}
.runtime-item {{
    background: white;
    padding: 12px;
    border-radius: 4px;
    border-left: 3px solid #3498db;
}}
.runtime-label {{
    font-weight: bold;
    color: #34495e;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 5px;
}}
.runtime-value {{
    color: #555;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    word-break: break-word;
    padding: 8px;
    background: #f9f9f9;
    border-radius: 3px;
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

"""

    # Add runtime context section if available
    if runtime_context:
        entrypoint = runtime_context.get("entrypoint") or []
        cmd = runtime_context.get("cmd") or []

        # Handle user field - can be string or object
        user_data = runtime_context.get("user", "root")
        if isinstance(user_data, dict):
            user = user_data.get("value") or "root"
        else:
            user = user_data or "root"

        exposed_ports = runtime_context.get("exposed_ports") or []

        runtime_html = """<h2>Container Runtime Configuration</h2>
<div class="runtime-context">
    <div class="runtime-grid">
        <div class="runtime-item">
            <div class="runtime-label">Entrypoint</div>
            <div class="runtime-value">""" + (", ".join(entrypoint) if entrypoint else "None") + """</div>
        </div>
        <div class="runtime-item">
            <div class="runtime-label">Command</div>
            <div class="runtime-value">""" + (", ".join(cmd) if cmd else "None") + """</div>
        </div>
        <div class="runtime-item">
            <div class="runtime-label">User</div>
            <div class="runtime-value">""" + user + """</div>
        </div>
        <div class="runtime-item">
            <div class="runtime-label">Exposed Ports</div>
            <div class="runtime-value">""" + (", ".join(exposed_ports) if exposed_ports else "None") + """</div>
        </div>
    </div>
</div>

"""
        html += runtime_html

    html += """
<h2>Package Vulnerabilities</h2>

<div class="filters">
    <div class="filter-group">
        <label for="filterPackage">Package Name:</label>
        <input type="text" id="filterPackage" placeholder="Filter by package name...">
    </div>
    <div class="filter-group">
        <label for="filterVulnCount">Vulnerability Count:</label>
        <select id="filterVulnCount">
            <option value="">All</option>
            <option value="0">0 (No vulnerabilities)</option>
            <option value=">0">&gt; 0 (Has vulnerabilities)</option>
            <option value="1">Exactly 1</option>
            <option value="2">Exactly 2</option>
            <option value="3">Exactly 3</option>
            <option value=">3">&gt; 3</option>
        </select>
    </div>
    <div class="filter-group">
        <button onclick="resetFilters()">Reset Filters</button>
    </div>
</div>

<table id="vulnTable">
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

        # Get usage context if available
        usage_context = pkg.get("usage_context", {})
        confidence = usage_context.get("confidence", "unknown") if usage_context else "unknown"
        used_at_runtime = usage_context.get("used_at_runtime", False) if usage_context else False

        row_class = "vulnerable" if vuln_count > 0 else ""

        # Build vulnerability details
        if vuln_count > 0:
            details_html = ""
            for vuln in vuln_items:
                vuln_id = vuln.get("id", "UNKNOWN")
                vuln_summary = vuln.get("summary", "No summary available")
                vuln_severity = vuln.get("severity", "Unknown")
                vuln_url = vuln.get("details_url", "#")
                patch_status = vuln.get("patch_status", "unknown")
                fixed_version = vuln.get("fixed_version", None)

                # New fields
                affected_ecosystem = vuln.get("affected_ecosystem", "")
                urgency_raw = vuln.get("urgency")
                urgency = (urgency_raw or "").lower() if urgency_raw else ""
                versions = vuln.get("versions", [])
                published = vuln.get("published", "")
                modified = vuln.get("modified", "")
                references = vuln.get("references", [])
                upstream = vuln.get("upstream", [])

                sev_class = severity_class(vuln_severity)

                # Determine patch status styling
                patch_class = "patch-available" if patch_status.lower() == "patched" else "patch-not-available"
                patch_text = "✓ Patch Available" if patch_status.lower() == "patched" else "✗ No Patch Available"

                # Build fixed version info
                fixed_version_html = ""
                if fixed_version:
                    fixed_version_html = f'<br><small style="color: #555;"><strong>Fixed in:</strong> <span class="fixed-version">{fixed_version}</span></small>'

                # Build urgency badge
                urgency_badge = ""
                if urgency:
                    urgency_class = f"urgency-{urgency}"
                    urgency_text = urgency.capitalize()
                    urgency_badge = f'<span class="{urgency_class}">{urgency_text}</span>'

                # Build versions list
                versions_html = ""
                if versions:
                    versions_text = ", ".join(versions[:5])  # Show first 5 versions
                    if len(versions) > 5:
                        versions_text += f", +{len(versions) - 5} more"
                    versions_html = f'<div class="meta-item"><span class="meta-label">Affected Versions</span><span class="meta-value"><code>{versions_text}</code></span></div>'

                # Build dates
                dates_html = ""
                date_parts = []
                if published:
                    date_parts.append(f'<div class="meta-item"><span class="meta-label">Published</span><span class="meta-value">{published}</span></div>')
                if modified:
                    date_parts.append(f'<div class="meta-item"><span class="meta-label">Modified</span><span class="meta-value">{modified}</span></div>')
                if date_parts:
                    dates_html = "".join(date_parts)

                # Build references list
                references_html = ""
                if references:
                    refs_list = ""
                    for ref in references[:3]:  # Show first 3 references
                        refs_list += f'<li><a href="{ref}" target="_blank">{ref[:60]}...</a></li>'
                    if len(references) > 3:
                        refs_list += f'<li><em>+{len(references) - 3} more references</em></li>'
                    references_html = f'<div class="meta-item"><span class="meta-label">References</span><ul class="references-list">{refs_list}</ul></div>'

                # Build upstream list
                upstream_html = ""
                if upstream:
                    upstream_text = ", ".join(upstream[:3])  # Show first 3
                    if len(upstream) > 3:
                        upstream_text += f", +{len(upstream) - 3} more"
                    upstream_html = f'<div class="meta-item"><span class="meta-label">Upstream</span><span class="meta-value">{upstream_text}</span></div>'

                # Build metadata section
                meta_html = ""
                if affected_ecosystem or urgency_badge or versions_html or dates_html or references_html or upstream_html:
                    meta_items = ""
                    if affected_ecosystem:
                        meta_items += f'<div class="meta-item"><span class="meta-label">Ecosystem</span><span class="meta-value">{affected_ecosystem}</span></div>'
                    if urgency_badge:
                        meta_items += f'<div class="meta-item"><span class="meta-label">Urgency</span><span class="meta-value">{urgency_badge}</span></div>'
                    meta_items += versions_html
                    meta_items += dates_html
                    meta_items += upstream_html
                    meta_html = f'<div class="vuln-meta">{meta_items}{references_html}</div>'

                details_html += f"""
                <div class="vuln-item">
                    <span class="badge {sev_class}">{vuln_id}</span><br>
                    <small style="color: #555;">{vuln_summary}</small><br>
                    <small style="color: #7f8c8d;"><strong>Severity:</strong> {vuln_severity}</small><br>
                    <span class="patch-status {patch_class}">{patch_text}</span>{fixed_version_html}
                    {meta_html}
                    <br><a href="{vuln_url}" target="_blank">🔗 View details</a>
                </div>
                """
        else:
            details_html = '<span style="color: #27ae60;">✓ No known vulnerabilities</span>'

        # Build usage context badge
        usage_badge = ""
        if usage_context:
            runtime_indicator = "🔴 Runtime Used" if used_at_runtime else "⚪ Build Time"
            confidence_class = f"confidence-{confidence}".lower()
            usage_badge = f'<br><small style="margin-top: 8px; display: block;"><strong>Usage:</strong> {runtime_indicator} | Confidence: <span style="font-weight: bold;">{confidence}</span></small>'

        html += f"""
<tr class="{row_class}" data-package="{pkg_name.lower()}" data-vuln-count="{vuln_count}">
    <td><strong>{pkg_name}</strong>{usage_badge}</td>
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

<script>
// Filter functionality
function filterTable() {{
    const packageFilter = document.getElementById('filterPackage').value.toLowerCase();
    const vulnCountFilter = document.getElementById('filterVulnCount').value;
    
    const rows = document.querySelectorAll('#vulnTable tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {{
        const packageName = row.getAttribute('data-package');
        const vulnCount = parseInt(row.getAttribute('data-vuln-count'));
        
        let showRow = true;
        
        // Filter by package name
        if (packageFilter && !packageName.includes(packageFilter)) {{
            showRow = false;
        }}
        
        // Filter by vulnerability count
        if (vulnCountFilter) {{
            if (vulnCountFilter === '0' && vulnCount !== 0) {{
                showRow = false;
            }} else if (vulnCountFilter === '>0' && vulnCount === 0) {{
                showRow = false;
            }} else if (vulnCountFilter === '1' && vulnCount !== 1) {{
                showRow = false;
            }} else if (vulnCountFilter === '2' && vulnCount !== 2) {{
                showRow = false;
            }} else if (vulnCountFilter === '3' && vulnCount !== 3) {{
                showRow = false;
            }} else if (vulnCountFilter === '>3' && vulnCount <= 3) {{
                showRow = false;
            }}
        }}
        
        row.style.display = showRow ? '' : 'none';
        if (showRow) visibleCount++;
    }});
    
    // Show "no results" message if no rows are visible
    const existingNoResults = document.querySelector('.no-results');
    if (existingNoResults) {{
        existingNoResults.remove();
    }}
    
    if (visibleCount === 0) {{
        const table = document.getElementById('vulnTable');
        const noResultsDiv = document.createElement('div');
        noResultsDiv.className = 'no-results';
        noResultsDiv.textContent = 'No packages match the selected filters.';
        table.parentNode.insertBefore(noResultsDiv, table.nextSibling);
    }}
}}

function resetFilters() {{
    document.getElementById('filterPackage').value = '';
    document.getElementById('filterVulnCount').value = '';
    filterTable();
}}

// Attach event listeners
document.getElementById('filterPackage').addEventListener('input', filterTable);
document.getElementById('filterVulnCount').addEventListener('change', filterTable);
</script>

</body>
</html>
"""

    # Write HTML file
    output_file = output_dir / "vulnerability_report.html"
    output_file.write_text(html, encoding="utf-8")

    Logger().info(f"HTML report generated: {output_file.resolve()}")

    return output_file

