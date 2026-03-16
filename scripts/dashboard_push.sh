#!/bin/bash
# Dashboard Auto-Push Script
# Runs every 30 minutes to push dashboard data updates

DASHBOARD_DIR="$HOME/.openclaw/workspace/dashboard"
LOG_FILE="$HOME/.openclaw/dashboard_push.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cd "$DASHBOARD_DIR" || {
    echo "[$TIMESTAMP] ERROR: Cannot cd to $DASHBOARD_DIR" >> "$LOG_FILE"
    exit 1
}

# Check if there are any changes
if [ -z "$(git status --porcelain)" ]; then
    echo "[$TIMESTAMP] No changes to push" >> "$LOG_FILE"
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
git commit -m "Auto: data update $TIMESTAMP"

# Push to origin (PAT embedded in remote URL)
if git push origin master; then
    echo "[$TIMESTAMP] SUCCESS: Pushed dashboard updates" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] FAILED: Push failed" >> "$LOG_FILE"
    exit 1
fi

exit 0
