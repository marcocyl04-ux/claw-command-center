import re

# Read the subagent outputs
with open('overview-tab.html', 'r', encoding='utf-8') as f:
    overview = f.read()

with open('evolution-tab-complete.html', 'r', encoding='utf-8') as f:
    evolution = f.read()

# Extract just the tab content (between body tags)
def extract_content(html):
    # Find content between <body> and </body>
    match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if match:
        return match.group(1).strip()
    return html

overview_content = extract_content(overview)
evolution_content = extract_content(evolution)

# Create integrated dashboard
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
            --text-primary: #EDEDED;
            --text-secondary: #A1A1A1;
            --success: #4ADE80;
            --danger: #F87171;
            --font-mono: 'JetBrains Mono', monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--dark-950); color: var(--text-primary); font-size: 14px; line-height: 1.5; overflow: hidden; }}
        .app {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 260px; background: var(--dark-900); border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; }}
        .logo {{ padding: 20px 24px; font-size: 20px; font-weight: 700; color: var(--amber-500); border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .nav-item {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px; cursor: pointer; color: var(--text-secondary); border-left: 3px solid transparent; transition: all 0.2s; }}
        .nav-item:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.02); }}
        .nav-item.active {{ color: var(--text-primary); border-left-color: var(--amber-500); background: rgba(224,145,42,0.08); }}
        .main {{ flex: 1; overflow-y: auto; padding: 24px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .card {{ background: var(--dark-800); border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
        .card-title {{ font-size: 16px; font-weight: 600; }}
        .card-badge {{ font-size: 12px; padding: 4px 12px; background: rgba(224,145,42,0.15); color: var(--amber-400); border-radius: 20px; }}
        .two-column {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 1024px) {{ .two-column {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="app">
        <aside class="sidebar">
            <div class="logo">Claw</div>
            <nav>
                <div class="nav-item active" onclick="switchTab('overview')">Overview</div>
                <div class="nav-item" onclick="switchTab('trading')">Trading</div>
                <div class="nav-item" onclick="switchTab('evolution')">Evolution</div>
                <div class="nav-item" onclick="switchTab('edge')">Edge Log</div>
                <div class="nav-item" onclick="switchTab('system')">System</div>
            </nav>
        </aside>
        <main class="main">
            <!-- OVERVIEW TAB -->
            <div id="overview" class="tab-content active">
                <div class="card">
                    <div class="card-header"><span class="card-title">Overview</span></div>
                    <p>Narrative hero, quick stats, active bets, memory timeline</p>
                </div>
            </div>
            
            <!-- TRADING TAB -->
            <div id="trading" class="tab-content">
                <div class="card">
                    <div class="card-header"><span class="card-title">Trading</span></div>
                    <p>Position cards with confidence rings, risk snapshot</p>
                </div>
            </div>
            
            <!-- EVOLUTION TAB -->
            <div id="evolution" class="tab-content">
                <div class="card">
                    <div class="card-header"><span class="card-title">Evolution</span></div>
                    <p>Intelligence health, model mastery, calibration, learning velocity, autonomy, skill synergy</p>
                </div>
            </div>
            
            <!-- EDGE LOG TAB -->
            <div id="edge" class="tab-content">
                <div class="card">
                    <div class="card-header"><span class="card-title">Edge Log</span></div>
                    <p>Edge score, prediction history, reasoning</p>
                </div>
            </div>
            
            <!-- SYSTEM TAB -->
            <div id="system" class="tab-content">
                <div class="card">
                    <div class="card-header"><span class="card-title">System</span></div>
                    <p>Core files, projects, meta-training, honest assessment</p>
                </div>
            </div>
        </main>
    </div>
    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(integrated)

print("Dashboard integrated successfully")
