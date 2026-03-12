"""
Optional: run as a background process that triggers at morning and evening times.
Alternative to Windows Task Scheduler. Stays running and fires at configured times.
"""
import time
import threading
from datetime import datetime
from pathlib import Path

# Ensure project root is on path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_once import main as run_once


def load_config():
    import json
    with open(Path(__file__).parent / "config.json", encoding="utf-8") as f:
        return json.load(f)


def parse_time(s: str):
    """Parse 'HH:MM' to (hour, minute)."""
    h, m = s.split(":")
    return int(h), int(m)


def next_run_seconds(morning: tuple, evening: tuple) -> float:
    """Seconds until the next scheduled run (morning or evening)."""
    from datetime import timedelta
    now = datetime.now()
    soonest = None
    for h, m in [morning, evening]:
        target = datetime(now.year, now.month, now.day, h, m)
        if target <= now:
            target += timedelta(days=1)
        sec = (target - now).total_seconds()
        if soonest is None or sec < soonest:
            soonest = sec
    return soonest or 60.0


def run_at_schedule():
    config = load_config()
    schedule = config.get("schedule", {})
    morning = parse_time(schedule.get("morning_time", "09:00"))
    evening = parse_time(schedule.get("evening_time", "18:00"))

    print(f"Scheduler started. Morning at {schedule.get('morning_time')}, evening at {schedule.get('evening_time')}.")
    while True:
        delay = next_run_seconds(morning, evening)
        print(f"Next run in {delay / 60:.0f} minutes.")
        time.sleep(delay)
        print("Running scheduled fetch...")
        run_once()


if __name__ == "__main__":
    run_at_schedule()
