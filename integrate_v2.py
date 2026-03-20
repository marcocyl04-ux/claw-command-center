import re

# Read subagent files
with open('overview-tab.html', 'r', encoding='utf-8') as f:
    overview_html = f.read()

with open('evolution-tab-complete.html', 'r', encoding='utf-8') as f:
    evolution_html = f.read()

# Extract content between body tags more simply
overview_body = overview_html.split('</style>')[-1] if '</style>' in overview_html else overview_html
overview_body = overview_body.replace('<body>', '').replace('</body>', '').strip()
if overview_body.startswith('>'):
    overview_body = overview_body[1:].strip()

evolution_body = evolution_html.split('</style>')[-1] if '</style>' in evolution_html else evolution_html
evolution_body = evolution_body.replace('<body>', '').replace('</body>', '').strip()
if evolution_body.startswith('>'):
    evolution_body = evolution_body[1:].strip()

# Extract just the inner content (remove outer divs if present)
overview_body = re.sub(r'^<div[^>]*>', '', overview_body)
overview_body = re.sub(r'</div>\s*$', '', overview_body)

evolution_body = re.sub(r'^<div[^>]*>', '', evolution_body)
evolution_body = re.sub(r'</div>\s*$', '', evolution_body)

# Extract CSS
overview_css = re.search(r'<style>(.*?)</style>', overview_html, re.DOTALL)
overview_css = overview_css.group(1) if overview_css else ""

evolution_css = re.search(r'<style>(.*?)</style>', evolution_html, re.DOTALL)
evolution_css = evolution_css.group(1) if evolution_css else ""

print(f"Overview CSS: {len(overview_css)} chars")
print(f"Overview body: {len(overview_body)} chars")
print(f"Evolution CSS: {len(evolution_css)} chars")
print(f"Evolution body: {len(evolution_body)} chars")

# Build integrated dashboard
integrated = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claw Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --amber-500: #E0912A;
            --amber-400: #F5A94C;
            --dark-950: #0A0A0A;
            --dark-900: #141414;
            --dark-800: #1A1A1A;
            --dark-700: #262626;
            --text-primary: #EDEDED;
            --text-secondary: #A1A1A1;
            --text-tertiary: #6B6B6B;
            --success: #4ADE80;
            --danger: #F87171;
            --font-mono: 'JetBrains Mono', monospace;
            --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 20px; --space-6: 24px;
            --text-xs: 11px; --text-sm: 13px; --text-base: 14px; --text-lg: 16px; --text-xl: 20px; --text-2xl: 28px;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--dark-950); color: var(--text-primary); font-size: 14px; line-height: 1.5; overflow: hidden; }}
        .app {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 260px; background: var(--dark-900); border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; flex-shrink: 0; }}
        .logo {{ padding: 20px 24px; font-size: 20px; font-weight: 700; color: var(--amber-500); border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .nav-item {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px; cursor: pointer; color: var(--text-secondary); border-left: 3px solid transparent; transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease; background: none; border: none; width: 100%; text-align: left; font-size: 14px; }}
        .nav-item:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.02); }}
        .nav-item.active {{ color: var(--text-primary); border-left-color: var(--amber-500); background: rgba(224,145,42,0.08); }}
        .nav-item:focus-visible {{ outline: 2px solid var(--amber-500); outline-offset: -2px; }}
        .main {{ flex: 1; overflow-y: auto; padding: 24px; min-width: 0; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .main::-webkit-scrollbar {{ width: 6px; }}
        .main::-webkit-scrollbar-track {{ background: transparent; }}
        .main::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 3px; }}
        @media (max-width: 1024px) {{ .sidebar {{ width: 72px; }} .nav-item span {{ display: none; }} }}
        @media (max-width: 768px) {{ .sidebar {{ position: fixed; left: 0; top: 0; bottom: 0; transform: translateX(-100%); z-index: 50; transition: transform 0.3s; }} .sidebar.open {{ transform: translateX(0); }} .main {{ padding: 16px; }} }}
        
        /* Overview Styles */
        {overview_css}
        
        /* Evolution Styles */
        {evolution_css}
    </style>
</head>
<body>
    <div class="app">
        <aside class="sidebar" role="navigation" aria-label="Main navigation">
            <div class="logo">🐾 Claw</div>
            <nav>
                <button class="nav-item active" onclick="switchTab('overview')" aria-label="Overview tab" aria-selected="true" role="tab"><span>📊 Overview</span></button>
                <button class="nav-item" onclick="switchTab('trading')" aria-label="Trading tab" role="tab"><span>📈 Trading</span></button>
                <button class="nav-item" onclick="switchTab('evolution')" aria-label="Evolution tab" role="tab"><span>🧠 Evolution</span></button>
                <button class="nav-item" onclick="switchTab('edge')" aria-label="Edge Log tab" role="tab"><span>⚡ Edge Log</span></button>
                <button class="nav-item" onclick="switchTab('system')" aria-label="System tab" role="tab"><span>⚙️ System</span></button>
            </nav>
        </aside>
        <main class="main" role="main">
            <div id="overview" class="tab-content active" role="tabpanel" aria-labelledby="tab-overview">
                <div class="claw-overview">
                    {overview_body}
                </div>
            </div>
            <div id="trading" class="tab-content" role="tabpanel">
                <div style="padding: 40px; text-align: center; color: var(--text-secondary);"><h2>Trading Tab</h2><p>Position cards and risk metrics loading...</p></div>
            </div>
            <div id="evolution" class="tab-content" role="tabpanel">
                {evolution_body}
            </div>
            <div id="edge" class="tab-content" role="tabpanel">
                <div style="padding: 40px; text-align: center; color: var(--text-secondary);"><h2>Edge Log</h2><p>Edge score and prediction history loading...</p></div>
            </div>
            <div id="system" class="tab-content" role="tabpanel">
                <div style="padding: 40px; text-align: center; color: var(--text-secondary);"><h2>System</h2><p>Core files and meta-training loading...</p></div>
            </div>
        </main>
    </div>
    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(tab => {{ tab.classList.remove('active'); tab.setAttribute('aria-hidden', 'true'); }});
            const selectedTab = document.getElementById(tabId);
            if (selectedTab) {{ selectedTab.classList.add('active'); selectedTab.setAttribute('aria-hidden', 'false'); }}
            document.querySelectorAll('.nav-item').forEach(item => {{ item.classList.remove('active'); item.setAttribute('aria-selected', 'false'); }});
            if (event && event.target) {{ event.target.classList.add('active'); event.target.setAttribute('aria-selected', 'true'); }}
        }}
        document.addEventListener('keydown', (e) => {{ if (e.key >= '1' && e.key <= '5') {{ const tabs = ['overview', 'trading', 'evolution', 'edge', 'system']; const index = parseInt(e.key) - 1; if (tabs[index]) switchTab(tabs[index]); }} }});
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(integrated)

print(f"\n✓ Dashboard integrated: {len(integrated):,} characters")
