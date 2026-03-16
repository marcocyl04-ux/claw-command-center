# Dashboard Auto-Push Script for Windows
# Runs every 30 minutes to push dashboard data updates

$DASHBOARD_DIR = "$env:USERPROFILE\.openclaw\workspace\dashboard"
$LOG_FILE = "$env:USERPROFILE\.openclaw\dashboard_push.log"
$TIMESTAMP = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

try {
    Set-Location $DASHBOARD_DIR
    
    # Check if there are any changes
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Add-Content $LOG_FILE "[$TIMESTAMP] No changes to push"
        exit 0
    }
    
    # Add all changes
    git add -A
    
    # Commit with timestamp
    git commit -m "Auto: data update $TIMESTAMP"
    
    # Push to origin
    $pushOutput = git push origin master 2>&1
    if ($LASTEXITCODE -eq 0) {
        Add-Content $LOG_FILE "[$TIMESTAMP] SUCCESS: Pushed dashboard updates"
    } else {
        Add-Content $LOG_FILE "[$TIMESTAMP] FAILED: Push failed - $pushOutput"
        exit 1
    }
} catch {
    Add-Content $LOG_FILE "[$TIMESTAMP] ERROR: $_"
    exit 1
}

exit 0
