import json
from datetime import datetime
from pathlib import Path

ACTIVITY_FILE = Path("C:/Users/marco/.openclaw/workspace/claw-command-center/activity.json")

def log_activity(text, highlights=None, activity_type="system"):
    """Log an activity to the activity feed.
    
    Args:
        text: Natural language description of what happened
        highlights: List of words/phrases to highlight in amber
        activity_type: system | model | skill | subagent | decision | complete
    """
    try:
        # Read existing activities
        if ACTIVITY_FILE.exists():
            with open(ACTIVITY_FILE, 'r') as f:
                activities = json.load(f)
        else:
            activities = []
        
        # Create new activity
        now = datetime.now()
        hour = now.hour % 12 if now.hour % 12 != 0 else 12
        ampm = "AM" if now.hour < 12 else "PM"
        new_activity = {
            "timestamp": now.isoformat() + "Z",
            "time": f"{hour}:{now.minute:02d} {ampm}",
            "type": activity_type,
            "text": text,
            "highlights": highlights or []
        }
        
        # Add to front (newest first)
        activities.insert(0, new_activity)
        
        # Keep only last 20 activities
        activities = activities[:20]
        
        # Write back
        with open(ACTIVITY_FILE, 'w') as f:
            json.dump(activities, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Failed to log activity: {e}")
        return False

def log_skill_usage(skill_name, task_description):
    """Log when a skill is used."""
    return log_activity(
        f"Using {skill_name} to {task_description}",
        highlights=[skill_name],
        activity_type="skill"
    )

def log_model_routing(model_name, reason):
    """Log when switching/routing to a model."""
    return log_activity(
        f"Routing to {model_name} for {reason}",
        highlights=[model_name],
        activity_type="model"
    )

def log_subagent_spawn(agent_type, task):
    """Log when spawning a sub-agent."""
    return log_activity(
        f"Spawning {agent_type} to {task}",
        highlights=[agent_type],
        activity_type="subagent"
    )

def log_decision(description):
    """Log a decision point."""
    return log_activity(
        f"Decided: {description}",
        activity_type="decision"
    )

def log_complete(task, result):
    """Log task completion."""
    return log_activity(
        f"Complete: {task} — {result}",
        highlights=["Complete"],
        activity_type="complete"
    )

# Test: Log what I'm doing right now
if __name__ == "__main__":
    log_activity("Building activity logger function", ["activity logger"], "system")
    print("Activity logged successfully")
