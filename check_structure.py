# Check HTML structure
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all tab-content divs
import re
tabs = re.findall(r'<div id="(\w+)" class="tab-content', html)
print(f"Tabs found: {tabs}")

# Check if each tab is properly closed
for tab in tabs:
    # Find opening position
    open_match = re.search(rf'<div id="{tab}" class="tab-content[^"]*">', html)
    if open_match:
        open_pos = open_match.end()
        # Find the next tab or end of main
        remaining = html[open_pos:]
        # Count div opens and closes to find matching close
        depth = 1
        pos = 0
        while depth > 0 and pos < len(remaining):
            next_open = remaining.find('<div', pos)
            next_close = remaining.find('</div>', pos)
            
            if next_close == -1:
                print(f"  {tab}: NO CLOSING TAG FOUND!")
                break
            
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
                if depth == 0:
                    print(f"  {tab}: properly closed at position {open_pos + pos}")
                    break

# Check overall structure between tabs
overview_end = html.find('<div id="trading"')
evolution_start = html.find('<div id="evolution"')
evolution_end = html.find('<div id="trading"', evolution_start + 1)

print(f"\nOverview ends at: {overview_end}")
print(f"Evolution starts at: {evolution_start}")
print(f"Evolution ends at: {evolution_end}")

if overview_end > evolution_start:
    print("ERROR: Evolution starts BEFORE Overview ends (nested!)")
else:
    print("Structure: Overview → Evolution → Trading (sequential)")
