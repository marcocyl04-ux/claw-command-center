#!/usr/bin/env python3
"""Minimal dashboard server - Sprint 8 Phase 1"""

from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

OPENCLAW_DIR = Path.home() / ".openclaw"

@app.route('/')
def index():
    """Serve the dashboard HTML."""
    dashboard_path = Path(__file__).parent / "index.html"
    if dashboard_path.exists():
        return dashboard_path.read_text()
    return "Dashboard not found", 404

@app.route('/api/predictions')
def get_predictions():
    """Return last 20 predictions from predictions.jsonl."""
    predictions_file = OPENCLAW_DIR / "predictions.jsonl"
    predictions = []
    
    if predictions_file.exists():
        with open(predictions_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        predictions.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    # Return last 20, most recent first
    return jsonify(predictions[-20:][::-1])

@app.route('/api/heuristics')
def get_heuristics():
    """Return parsed heuristics from heuristics.md."""
    heuristics_file = OPENCLAW_DIR / "heuristics.md"
    heuristics = []
    
    if heuristics_file.exists():
        content = heuristics_file.read_text()
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- [UNVALIDATED]') or line.startswith('- [VALIDATED]'):
                status = "UNVALIDATED" if "UNVALIDATED" in line else "VALIDATED"
                text = line.replace('- [UNVALIDATED]', '').replace('- [VALIDATED]', '').strip()
                heuristics.append({
                    "text": text,
                    "status": status,
                    "trigger_count": 0,  # TODO: calculate from actual data
                    "last_triggered": None
                })
    
    return jsonify(heuristics)

@app.route('/api/self-review')
def get_self_review():
    """Return last 5 self-review entries from review_log.jsonl."""
    review_file = OPENCLAW_DIR / "review_log.jsonl"
    reviews = []
    
    if review_file.exists():
        with open(review_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        reviews.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    return jsonify(reviews[-5:][::-1])

@app.route('/api/portfolio')
def get_portfolio():
    """Return portfolio data (placeholder until real source found)."""
    # TODO: Replace with actual portfolio data source
    return jsonify({
        "source": "TBD",
        "deployed": 45.27,
        "total": 50.00,
        "realized_pnl": 3.42,
        "win_rate": 0.71,
        "resolved": 7,
        "wins": 5,
        "losses": 2,
        "open_positions": 12,
        "positions": [
            {"market": "NYC temp > 18°C Mar 18", "direction": "YES", "edge": 0.12, "deployed": 4.00, "days_left": 2},
            {"market": "London precip Mar 19", "direction": "NO", "edge": 0.08, "deployed": 3.50, "days_left": 3},
            {"market": "Tokyo temp > 22°C Mar 20", "direction": "YES", "edge": 0.15, "deployed": 5.00, "days_left": 4},
            {"market": "Sydney temp < 25°C Mar 21", "direction": "YES", "edge": 0.06, "deployed": 2.75, "days_left": 5},
            {"market": "Paris precip Mar 22", "direction": "NO", "edge": 0.10, "deployed": 4.25, "days_left": 6}
        ]
    })

@app.route('/api/evolution')
def get_evolution():
    """Return last 10 evolution entries from PROGRESS.md."""
    progress_file = Path(__file__).parent / "PROGRESS.md"
    entries = []
    
    if progress_file.exists():
        content = progress_file.read_text()
        # Simple parsing - look for Sprint headers
        lines = content.split('\n')
        current_entry = None
        
        for line in lines:
            if line.startswith('## Sprint'):
                if current_entry:
                    entries.append(current_entry)
                current_entry = {
                    "title": line.replace('## ', '').strip(),
                    "details": []
                }
            elif current_entry and line.strip().startswith('-'):
                current_entry["details"].append(line.strip())
        
        if current_entry:
            entries.append(current_entry)
    
    return jsonify(entries[-10:][::-1])

@app.route('/api/activation-map')
def get_activation_map():
    """Return last 20 subagent calls from subagent_calls.jsonl."""
    calls_file = OPENCLAW_DIR / "subagent_calls.jsonl"
    calls = []
    
    if calls_file.exists():
        with open(calls_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        calls.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    
    return jsonify(calls[-20:][::-1])

if __name__ == '__main__':
    print("Dashboard server starting on http://localhost:5000")
    print("Endpoints:")
    print("  GET /api/predictions")
    print("  GET /api/heuristics")
    print("  GET /api/self-review")
    print("  GET /api/portfolio")
    print("  GET /api/evolution")
    print("  GET /api/activation-map")
    app.run(host='0.0.0.0', port=5000, debug=False)
