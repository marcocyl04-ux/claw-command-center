# Auto-Export Dashboard Data

This script automatically exports your OpenClaw data and pushes it to GitHub for the dashboard.

## Setup (One-time)

### 1. Make script executable
```bash
chmod +x export-dashboard-data.sh
```

### 2. Install as cron job (runs every 30 minutes)
```bash
# Edit crontab
crontab -e

# Add this line:
*/30 * * * * cd ~/claw-command-center && ./export-dashboard-data.sh >> ~/dashboard-export.log 2>&1
```

### 3. Or run manually when you want updates
```bash
./export-dashboard-data.sh
```

## How it works

1. Reads your local files: SOUL.md, MEMORY.md, USER.md, AGENTS.md
2. Compiles dashboard data
3. Saves to dashboard-data.json
4. Commits and pushes to GitHub
5. Dashboard loads fresh data on next visit

## View logs

```bash
tail -f ~/dashboard-export.log
```

## Disable auto-export

```bash
crontab -e
# Remove the line with export-dashboard-data.sh
```