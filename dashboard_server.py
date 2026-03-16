"""
dashboard_server.py
Simple Flask server to serve the Claw performance dashboard.
"""

from flask import Flask, send_from_directory, jsonify
from pathlib import Path
import json
import re
from datetime import datetime

app = Flask(__name__)

# Paths
DASHBOARD_DIR = Path(__file__).parent
WORKSPACE_DIR = DASHBOARD_DIR.parent
PERFORMANCE_LOG = WORKSPACE_DIR / "performance.log"


def parse_performance_log():
    """Parse performance.log and return dashboard data."""
    predictions = []
    
    if not PERFORMANCE_LOG.exists():
        return {
            "totalPredictions": 0,
            "accuracy": 0,
            "avgConfidence": 0,
            "calibration": 1.0,
            "recentPredictions": []
        }
    
    try:
        with open(PERFORMANCE_LOG, 'r') as f:
            content = f.read()
        
        # Parse prediction entries
        # Format: [2026-03-14 04:41:47] Accuracy: 0.0%, Avg Confidence: 0.00
        pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] Accuracy: ([\d.]+)%, Avg Confidence: ([\d.]+)'
        matches = re.findall(pattern, content)
        
        if matches:
            latest = matches[-1]
            accuracy = float(latest[1])
            avg_confidence = float(latest[2])
        else:
            accuracy = 0
            avg_confidence = 0
        
        # Count predictions (from predictions.jsonl if exists)
        predictions_file = WORKSPACE_DIR / "predictions.jsonl"
        total = 0
        if predictions_file.exists():
            with open(predictions_file, 'r') as f:
                total = sum(1 for line in f if line.strip())
        
        # Mock recent predictions (in production, parse from predictions.jsonl)
        recent = [
            {"market": "SpaceX Flight 13", "recommendation": "NO TRADE", "predicted": "NO", "confidence": 0.35, "outcome": None, "status": "pending"},
            {"market": "NYC Temp Mar 20", "recommendation": "TRADE", "predicted": "NO", "confidence": 0.72, "outcome": "NO", "status": "correct"},
            {"market": "Crypto ETF", "recommendation": "NO TRADE", "predicted": "NO", "confidence": 0.28, "outcome": "NO", "status": "correct"},
            {"market": "Rain LA", "recommendation": "WAIT", "predicted": "YES", "confidence": 0.50, "outcome": "NO", "status": "incorrect"},
            {"market": "Starship Launch", "recommendation": "TRADE", "predicted": "YES", "confidence": 0.68, "outcome": "YES", "status": "correct"},
        ]
        
        return {
            "totalPredictions": total or len(recent),
            "accuracy": accuracy,
            "avgConfidence": avg_confidence,
            "calibration": 1.0,  # Would calculate from historical data
            "recentPredictions": recent
        }
        
    except Exception as e:
        print(f"Error parsing performance log: {e}")
        return {
            "totalPredictions": 0,
            "accuracy": 0,
            "avgConfidence": 0,
            "calibration": 1.0,
            "recentPredictions": [],
            "error": str(e)
        }


@app.route('/')
def index():
    """Serve the dashboard HTML."""
    return send_from_directory(DASHBOARD_DIR, 'index.html')


@app.route('/api/dashboard')
def dashboard_data():
    """Return dashboard data as JSON."""
    return jsonify(parse_performance_log())


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory(DASHBOARD_DIR, filename)


if __name__ == '__main__':
    print("=" * 60)
    print("Claw Performance Dashboard Server")
    print("=" * 60)
    print(f"Dashboard: http://localhost:5000")
    print(f"API: http://localhost:5000/api/dashboard")
    print("=" * 60)
    app.run(debug=True, port=5000)
