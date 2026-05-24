<#
.SYNOPSIS
  One-shot "second window": load faerie env, refresh Obsidian queue mirror, start Mission Control (live JSON).

.DESCRIPTION
  Dot-sources ~/.claude/faerie-env.ps1 (from faerie-env.json), runs export_queue_to_vault.py if present,
  then launches dashboard.py --watch in a new process.

  Run after: install-faerie.ps1 (Core + Collab env). Double-click or run from PowerShell.
#>
$ErrorActionPreference = "Stop"

$envPs1 = Join-Path $env:USERPROFILE ".claude\faerie-env.ps1"
if (Test-Path $envPs1) {
    . $envPs1
} else {
    Write-Warning "Missing $envPs1 - run scripts\install\install-faerie.ps1 -CollabEnv or copy faerie-env.example.json to ~/.claude/faerie-env.json"
}

$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = Get-Command python3 -ErrorAction Stop }
$exe = $py.Source

$export = Join-Path $env:USERPROFILE ".claude\hooks\state\export_queue_to_vault.py"
if (Test-Path $export) {
    Write-Host "Refreshing vault queue mirror..."
    & $exe $export
}

$db = Join-Path $env:USERPROFILE ".claude\dashboard.py"
if (-not (Test-Path $db)) {
    Write-Error "dashboard.py not found at $db - install Core bundle first (install-faerie.ps1 -InstallCore)."
    exit 1
}

Write-Host "Starting Mission Control (dashboard --watch)..."
Start-Process -FilePath $exe -ArgumentList @($db, "--watch") -WindowStyle Normal
