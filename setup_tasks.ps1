# Create Windows scheduled tasks: morning and evening stock report.
# Run PowerShell as Administrator, then: .\setup_tasks.ps1

$ScriptDir = $PSScriptRoot
$PythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonExe) { $PythonExe = (Get-Command py -ErrorAction SilentlyContinue).Source }
if (-not $PythonExe) { Write-Host "Python not found. Install Python and add to PATH."; exit 1 }

$RunScript = Join-Path $ScriptDir "run_once.py"
$TaskName1 = "StockTrackerMorning"
$TaskName2 = "StockTrackerEvening"

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$RunScript`"" -WorkingDirectory $ScriptDir
$Trigger1 = New-ScheduledTaskTrigger -Daily -At "09:00"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "18:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName1 -Action $Action -Trigger $Trigger1 -Settings $Settings -Force
Register-ScheduledTask -TaskName $TaskName2 -Action $Action -Trigger $Trigger2 -Settings $Settings -Force

Write-Host "Tasks created: $TaskName1 (9:00), $TaskName2 (18:00)."
Write-Host "To change times, edit config.json and run this script again, or use Task Scheduler (taskschd.msc)."
