import re

# Read files
with open('overview-tab.html', 'r', encoding='utf-8') as f:
    overview = f.read()

with open('evolution-charts.html', 'r', encoding='utf-8') as f:
    evolution = f.read()

with open('trading-tab.html', 'r', encoding='utf-8') as f:
    trading = f.read()

# Extract overview CSS and body
overview_parts = overview.split('</style>')
overview_css = overview_parts[0].replace('<style>', '').strip() if len(overview_parts) > 0 else ""
overview_body = overview_parts[1].strip() if len(overview_parts) > 1 else ""
overview_body = re.sub(r'^<div[^>]*class="claw-overview"[^>]*>', '', overview_body)
overview_body = re.sub(r'</div>\s*$', '', overview_body).strip()

# Evolution is already clean HTML
evolution_body = evolution.strip()
evolution_css = ""  # Evolution uses inline styles

# Trading - extract between <main> and </main>
trading_match = re.search(r'<main[^>]*>(.*?)</main>', trading, re.DOTALL)
trading_body = trading_match.group(1).strip() if trading_match else ""
trading_body = re.sub(r'^<div[^>]*class="tab-content[^"]*"[^>]*>', '', trading_body)
trading_body = re.sub(r'</div>\s*$', '', trading_body).strip()
trading_css = ''.join(re.findall(r'<style>(.*?)</style>', trading, re.DOTALL))

print(f"Overview: {len(overview_css)} CSS, {len(overview_body)} body")
print(f"Evolution: {len(evolution_body)} body")
print(f"Trading: {len(trading_css)} CSS, {len(trading_body)} body")

# Build final
final = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claw Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{ --amber-500: #E0912A; --amber-400: #F5A94C; --dark-950: #0A0A0A; --dark-900: #141414; --dark-800: #1A1A1A; --text-primary: #EDEDED; --text-secondary: #A1A1A1; --success: #4ADE80; --danger: #F87171; --font-mono: 'JetBrains Mono', monospace; }}
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
        {overview_css}
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
                <div class="claw-overview">
                    {overview_body}
                </div>
            </div>
            <div id="trading" class="tab-content">
                {trading_body}
            </div>
            <div id="evolution" class="tab-content">
                {evolution_body}
            </div>
            <div id="edge" class="tab-content">
                <div style="padding: 40px; text-align: center; color: var(--text-secondary);">
                    <h2>Edge Log</h2>
                    <p style="font-size: 48px; font-family: var(--font-mono); color: var(--success); margin: 20px 0;">+12%</p>
                    <p>3 tested | 2 validated | 1 failed</p>
                </div>
            </div>
            <div id="system" class="tab-content">
                <div style="padding: 40px; text-align: center; color: var(--text-secondary);">
                    <h2>System</h2>
                    <p style="font-size: 36px; font-family: var(--font-mono); color: var(--amber-500); margin: 20px 0;">C+ → B-</p>
                    <p>Core Files: SOUL.md ✓ MEMORY.md ✓ AGENTS.md ✓ USER.md ✓</p>
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
    f.write(final)

print(f"\nDashboard: {len(final):,} characters")
print("Overview, Trading, Evolution integrated!")
