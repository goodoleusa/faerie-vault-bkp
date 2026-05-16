<#
.SYNOPSIS
  Writes ~/.claude/faerie-env.json and ~/.claude/faerie-env.ps1 from a hashtable.
  Internal helper - used by install-faerie.ps1
#>
param(
    [Parameter(Mandatory)][hashtable]$Config
)

$claudeHome = Join-Path $env:USERPROFILE ".claude"
New-Item -ItemType Directory -Force -Path $claudeHome | Out-Null

$jsonPath = Join-Path $claudeHome "faerie-env.json"
$out = [ordered]@{
    faerie_project_root = $Config.faerie_project_root
    flowsearch_repo     = $Config.flowsearch_repo
    faerie_vault_shared = $Config.faerie_vault_shared
    claude_hooks_state  = $Config.claude_hooks_state
    vault_drops         = $Config.vault_drops
}
$out | ConvertTo-Json -Depth 3 | Set-Content -Path $jsonPath -Encoding UTF8
Write-Host "Wrote $jsonPath"

$ps1 = @'
# Auto-generated - dot-source in PowerShell: . $env:USERPROFILE\.claude\faerie-env.ps1
$ErrorActionPreference = "Stop"
$p = Join-Path $env:USERPROFILE ".claude\faerie-env.json"
if (-not (Test-Path $p)) { return }
$j = Get-Content $p -Raw -Encoding UTF8 | ConvertFrom-Json
function Set-EnvIf([string]$name, [string]$val) {
    if ($val -and $val.Trim()) { Set-Item -Path "Env:$name" -Value $val.Trim() }
}
Set-EnvIf "FAERIE_PROJECT_ROOT" $j.faerie_project_root
Set-EnvIf "FAERIE_VAULT_SHARED" $j.faerie_vault_shared
Set-EnvIf "CLAUDE_HOOKS_STATE" $j.claude_hooks_state
Set-EnvIf "VAULT_DROPS" $j.vault_drops
'@

$ps1Path = Join-Path $claudeHome "faerie-env.ps1"
Set-Content -Path $ps1Path -Value $ps1 -Encoding UTF8
Write-Host "Wrote $ps1Path"

# Persist User-level env vars (optional - so new terminals inherit without dot-sourcing)
foreach ($pair in @(
        @{ Name = "FAERIE_PROJECT_ROOT"; Val = $Config.faerie_project_root }
        @{ Name = "FAERIE_VAULT_SHARED"; Val = $Config.faerie_vault_shared }
        @{ Name = "CLAUDE_HOOKS_STATE"; Val = $Config.claude_hooks_state }
        @{ Name = "VAULT_DROPS"; Val = $Config.vault_drops }
    )) {
    if ($pair.Val -and $pair.Val.Trim()) {
        [Environment]::SetEnvironmentVariable($pair.Name, $pair.Val.Trim(), "User")
        Write-Host "Set User env $($pair.Name)"
    }
}
