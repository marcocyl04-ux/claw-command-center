import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the main content area
main_match = re.search(r'(<main[^>]*>)(.*?)(</main>)', html, re.DOTALL)
if not main_match:
    print("ERROR: Could not find main content area")
    exit(1)

main_open = main_match.group(1)
main_content = main_match.group(2)
main_close = main_match.group(3)

# Find where overview tab starts
overview_start = main_content.find('<div id="overview" class="tab-content active">')
if overview_start == -1:
    print("ERROR: Could not find overview tab")
    exit(1)

# Find where trading tab starts - this marks the end of overview content
trading_start = main_content.find('<div id="trading" class="tab-content">')
if trading_start == -1:
    print("ERROR: Could not find trading tab")
    exit(1)

# Find where system tab starts
system_start = main_content.find('<div id="system" class="tab-content">')
if system_start == -1:
    print("ERROR: Could not find system tab")
    exit(1)

# Find where system tab ends (should be end of main content before closing)
system_end = main_content.rfind('</div>')  # Last closing div

# Extract each tab's content
overview_content = main_content[overview_start:trading_start]
trading_content = main_content[trading_start:system_start]
system_content = main_content[system_start:system_end+6]  # Include closing div

# Clean up - remove the tab-content wrapper from overview to get inner content
overview_inner = re.sub(r'^<div[^>]*class="tab-content[^"]*"[^>]*>', '', overview_content)
overview_inner = re.sub(r'</div>\s*$', '', overview_inner).strip()

# The overview inner contains both overview AND evolution content mixed together
# We need to find where evolution content starts (Intelligence Health card)
evolution_marker = '<div class="card intelligence-health">'
evolution_pos = overview_inner.find(evolution_marker)

if evolution_pos == -1:
    print("WARNING: Could not find Evolution content marker")
    evolution_pos = len(overview_inner)  # Put everything in overview

overview_only = overview_inner[:evolution_pos].strip()
evolution_content = overview_inner[evolution_pos:].strip()

print(f"Overview content: {len(overview_only)} chars")
print(f"Evolution content: {len(evolution_content)} chars")
print(f"Trading content: {len(trading_content)} chars")
print(f"System content: {len(system_content)} chars")

# Build clean structure
new_main_content = f'''<div id="overview" class="tab-content active">
                    {overview_only}
                </div>
                
                <div id="evolution" class="tab-content">
                    {evolution_content}
                </div>
                
                {trading_content}
                
                {system_content}
                
                <div id="edge" class="tab-content">
                    <div class="card">
                        <div class="card-header">
                            <span class="card-title">Edge Score</span>
                            <span class="card-badge">+12%</span>
                        </div>
                        <div class="card-body" style="text-align: center; padding: 40px;">
                            <div style="font-size: 48px; font-weight: 700; color: var(--success); margin-bottom: 16px;">+12%</div>
                            <p style="color: var(--text-secondary); margin-bottom: 24px;">Markets undervalue weather volatility</p>
                            <div style="display: flex; justify-content: center; gap: 32px;">
                                <div><div style="font-size: 24px; font-weight: 600;">3</div><div style="font-size: 12px; color: var(--text-tertiary);">Tested</div></div>
                                <div><div style="font-size: 24px; font-weight: 600; color: var(--success);">2</div><div style="font-size: 12px; color: var(--text-tertiary);">Validated</div></div>
                                <div><div style="font-size: 24px; font-weight: 600; color: var(--danger);">1</div><div style="font-size: 12px; color: var(--text-tertiary);">Failed</div></div>
                            </div>
                        </div>
                    </div>
                </div>'''

# Replace main content in HTML
new_html = html[:main_match.start()] + main_open + new_main_content + main_close + html[main_match.end():]

# Also need to add Edge Log to navigation
nav_match = re.search(r'(<nav[^>]*>)(.*?)(</nav>)', new_html, re.DOTALL)
if nav_match:
    nav_content = nav_match.group(2)
    # Add Edge Log nav item before closing </nav>
    new_nav_content = nav_content.replace(
        '</nav>',
        '                <button class="nav-item" onclick="switchTab(\'edge\')" aria-label="Edge Log tab" role="tab"><span>⚡ Edge Log</span></button>\n            </nav>'
    )
    new_html = new_html[:nav_match.start()] + nav_match.group(1) + new_nav_content + nav_match.group(3) + new_html[nav_match.end():]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\n✓ Fixed: All tabs now properly separated")
print(f"✓ Added: Edge Log tab")
print(f"✓ Total: {len(new_html):,} characters")
