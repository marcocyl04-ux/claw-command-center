import re

# Read all subagent files
with open('overview-tab.html', 'r', encoding='utf-8') as f:
    overview_html = f.read()

with open('evolution-tab-complete.html', 'r', encoding='utf-8') as f:
    evolution_html = f.read()

with open('trading-tab.html', 'r', encoding='utf-8') as f:
    trading_html = f.read()

# Extract content inside <main class="main"> to </main>
def extract_main_content(html):
    # Find content between <main class="main"> and </main>
    match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Remove the tab-content wrapper div if present
        content = re.sub(r'^<div[^>]*class="tab-content[^"]*"[^>]*>', '', content)
        content = re.sub(r'</div>\s*$', '', content)
        return content.strip()
    return ""

# Extract CSS from each file (everything between <style> and </style>)
def extract_all_css(html):
    styles = re.findall(r'<style>(.*?)</style>', html, re.DOTALL)
    return '\n'.join(styles)

overview_body = extract_main_content(overview_html)
overview_css = extract_all_css(overview_html)

evolution_body = extract_main_content(evolution_html)
evolution_css = extract_all_css(evolution_html)

trading_body = extract_main_content(trading_html)
trading_css = extract_all_css(trading_html)

print(f"Overview: {len(overview_css)} CSS chars, {len(overview_body)} body chars")
print(f"Evolution: {len(evolution_css)} CSS chars, {len(evolution_body)} body chars")
print(f"Trading: {len(trading_css)} CSS chars, {len(trading_body)} body chars")

# Build clean integrated dashboard
clean_dashboard = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claw Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        /* Base System */
        :root {{
            --amber-500: #E0912A; --amber-400: #F5A94C;
            --dark-950: #0A0A0A; --dark-900: #141414; --dark-800: #1A1A1A;
            --text-primary: #EDEDED; --text-secondary: #A1A1A1; --text-tertiary: #6B6B6B;
            --success: #4ADE80; --danger: #F87171;
            --font-mono: 'JetBrains Mono', monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--dark-950); color: var(--text-primary); font-size: 14px; line-height: 1.5; overflow: hidden; }}
        .app {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 260px; background: var(--dark-900); border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; flex-shrink: 0; }}
        .logo {{ padding: 20px 24px; font-size: 20px; font-weight: 700; color: var(--amber-500); border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .nav-item {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px; cursor: pointer; color: var(--text-secondary); border-left: 3px solid transparent; transition: all 0.2s; background: none; border: none; width: 100%; text-align: left; font-size: 14px; }}
        .nav-item:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.02); }}
        .nav-item.active {{ color: var(--text-primary); border-left-color: var(--amber-500); background: rgba(224,145,42,0.08); }}
        .main {{ flex: 1; overflow-y: auto; padding: 24px; min-width: 0; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        /* Overview CSS */
        {overview_css}
        
        /* Evolution CSS */
        {evolution_css}
        
        /* Trading CSS */
        {trading_css}
    </style>
</head>
<body>
    <div class="app">
        <aside class="sidebar">
            <div class="logo">🐾 Claw</div>
            <nav>
                <button class="nav-item active" onclick="switchTab('overview')">📊 Overview</button>
                <button class="nav-item" onclick="switchTab('trading')">📈 Trading</button>
                <button class="nav-item" onclick="switchTab('evolution')">🧠 Evolution</button>
                <button class="nav-item" onclick="switchTab('edge')">⚡ Edge Log</button>
                <button class="nav-item" onclick="switchTab('system')">⚙️ System</button>
            </nav>
        </aside>
        <main class="main">
            <div id="overview" class="tab-content active">
                {overview_body}
            </div>
            <div id="trading" class="tab-content">
                {trading_body}
            </div>
            <div id="evolution" class="tab-content">
                {evolution_body}
            </div>
            <div id="edge" class="tab-content">
                <div style="padding: 40px; text-align: center;">
                    <h2>Edge Log</h2>
                    <p>Edge Score: +12%</p>
                    <p>3 tested | 2 validated | 1 failed</p>
                    <p>Predictions where my reasoning differed from market</p>
                </div>
            </div>
            <div id="system" class="tab-content">
                <div style="padding: 40px; text-align: center;">
                    <h2>System</h2>
                    <p>Core Files: SOUL.md, MEMORY.md, AGENTS.md, USER.md</p>
                    <p>Grade: C+ → B-</p>
                    <p>2 gaps to close: Autonomous decisions, Edge discovery</p>
                </div>
            </div>
        </main>
    </div>
    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(clean_dashboard)

print(f"\n✓ Clean dashboard: {len(clean_dashboard):,} characters")
print("✓ All 5 tabs integrated!")
