# Auto-Export Dashboard Data - Windows Setup

## Manual Run (whenever you want)
```powershell
cd C:\Users\marco\.openclaw\workspace\claw-command-center
.\export-dashboard-data.ps1
```

## Automatic Setup (Every 30 minutes)

### Option 1: Task Scheduler (Recommended)
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Claw Dashboard Export"
4. Trigger: Every 30 minutes
5. Action: Start Program
6. Program: `powershell.exe`
7. Arguments: `-File "C:\Users\marco\.openclaw\workspace\claw-command-center\export-dashboard-data.ps1"`

### Option 2: Run in background now
```powershell
# Run this to start auto-export every 30 min
while ($true) {
    cd C:\Users\marco\.openclaw\workspace\claw-command-center
    .\export-dashboard-data.ps1
    Start-Sleep -Seconds 1800  # 30 minutes
}
```

## Check if it's working
Visit: https://marcocyl04-ux.github.io/claw-command-center/
Data updates within 1-2 minutes of each export.