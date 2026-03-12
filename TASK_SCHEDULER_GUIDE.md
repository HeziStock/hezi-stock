# HEZI STOCK – Windows Task Scheduler setup

Run HEZI STOCK automatically **twice a day** (e.g. morning and evening) without opening the app.

## Option 1: PowerShell script (recommended)

1. Open **PowerShell as Administrator**.
2. Go to the project folder, for example:
   ```powershell
   cd C:\Users\YourName\stock-tracker
   ```
3. Allow the script to run (this process only):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
4. Run the setup script:
   ```powershell
   .\setup_tasks.ps1
   ```
5. Two scheduled tasks are created: **HEZI STOCK Morning** and **HEZI STOCK Evening**.  
   Times are taken from `config.json` (`schedule.morning_time` and `schedule.evening_time`).  
   To change times, edit `config.json` and run `.\setup_tasks.ps1` again.

## Option 2: Manual setup in Task Scheduler

1. Press **Win + R**, type `taskschd.msc`, press Enter.
2. In the right panel, click **Create Basic Task**.
3. **Name:** e.g. `HEZI STOCK Morning`  
   **Description:** (optional) Run HEZI STOCK insight report.
4. **Trigger:** Daily → set time to **09:00** (or your preferred morning time).
5. **Action:** Start a program  
   - **Program:** `python`  
   - **Arguments:** `run_once.py`  
   - **Start in:** `C:\path\to\stock-tracker` (your project folder).
6. Finish. Repeat for evening (e.g. **18:00**) with a second task named `HEZI STOCK Evening`.

**Note:** If `python` is not in PATH for scheduled tasks, use the full path to `python.exe` (e.g. `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`).

## Option 3: Built-in scheduler (window must stay open)

```bash
python run_scheduler.py
```

Leave the window open. It runs at the morning and evening times in `config.json`. Closing the window stops the scheduler.
