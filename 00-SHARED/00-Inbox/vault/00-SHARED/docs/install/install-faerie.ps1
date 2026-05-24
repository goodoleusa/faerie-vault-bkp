<#
.SYNOPSIS
  Guided (or silent) install for faerie + optional collab env - modular, one place for setup.

.PARAMETER FlowsearchRoot
  Path to flowsearch repo root. Default: grandparent of scripts\install.

.PARAMETER ReleaseTarget
  windows-native | windows-wsl | linux | macos

.PARAMETER InstallCore
  Copy releases\<target>\orchestration\.claude\* → %USERPROFILE%\.claude (OSS default).
  Queue/dashboard/hooks/skills; excludes memory module (see modules/memory/manifest.private.json).

.PARAMETER InstallFull
  Copy releases\<target>\.claude\* → %USERPROFILE%\.claude — FULL combined bundle (s2 --profile full).
  Includes orchestration + memory module. Intended for paid / licensed distribution (memory is not a separate installer SKU).

.PARAMETER CollabEnv
  Write ~/.claude/faerie-env.json + faerie-env.ps1; set User env vars; copy start-faerie-workstation.ps1.

.PARAMETER Interactive
  Prompt for bundle (orchestration vs full) and paths.

.EXAMPLE
  .\install-faerie.ps1 -Interactive

.EXAMPLE
  .\install-faerie.ps1 -InstallCore -CollabEnv -FaerieProjectRoot "D:\path\to\project" -FaerieVaultShared "D:\path\to\flowsearch\ObsidianVault\00-SHARED"
#>
[CmdletBinding()]
param(
    [string]$FlowsearchRoot = "",
    [ValidateSet("windows-native", "windows-wsl", "linux", "macos")]
    [string]$ReleaseTarget = "windows-native",
    [switch]$InstallCore,
    [switch]$InstallFull,
    [switch]$CollabEnv,
    [switch]$Interactive,
    [string]$FaerieProjectRoot = "",
    [string]$FaerieVaultShared = "",
    [string]$ClaudeHooksState = "",
    [string]$VaultDrops = "",
    [switch]$SkipBackup
)

$ErrorActionPreference = "Stop"

if ($InstallCore -and $InstallFull) {
    Write-Error "Use only one of -InstallCore (orchestration OSS) or -InstallFull (paid combined)."
}

if (-not $FlowsearchRoot) {
    $FlowsearchRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

$dst = Join-Path $env:USERPROFILE ".claude"

if ($Interactive) {
    Write-Host "=== faerie + collab installer ===" -ForegroundColor Cyan
    $b = (Read-Host "Install bundle to ~/.claude? [O]rchestration open-source (default) | [F]ull combined (paid, includes memory) | [N]one").Trim()
    if ($b -match '^[fF]') { $InstallFull = $true }
    elseif ($b -match '^[nN]') { }
    else { $InstallCore = $true }
    $CollabEnv = $true

    $in = Read-Host "FAERIE_PROJECT_ROOT - your product repo path (optional)"
    if ($in.Trim()) { $FaerieProjectRoot = $in.Trim() }

    $defVault = Join-Path $FlowsearchRoot "ObsidianVault\00-SHARED"
    $in = Read-Host "FAERIE_VAULT_SHARED - 00-SHARED folder [$defVault]"
    if ($in.Trim()) { $FaerieVaultShared = $in.Trim() } else { $FaerieVaultShared = $defVault }

    $in = Read-Host "CLAUDE_HOOKS_STATE - optional shared team queue dir (Enter to skip)"
    if ($in.Trim()) { $ClaudeHooksState = $in.Trim() }

    $in = Read-Host "VAULT_DROPS - optional e.g. ...\00-SHARED\inbox\drops (Enter to skip)"
    if ($in.Trim()) { $VaultDrops = $in.Trim() }

    if ($InstallCore -or $InstallFull) {
        $in = Read-Host "Release target (windows-native|windows-wsl|linux|macos) [$ReleaseTarget]"
        if ($in.Trim()) { $ReleaseTarget = $in.Trim() }
    }
}

$orchSrc = Join-Path $FlowsearchRoot "releases\$ReleaseTarget\orchestration\.claude"
$fullSrc = Join-Path $FlowsearchRoot "releases\$ReleaseTarget\.claude"

function Install-FaerieBundle {
    param(
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][string]$Label
    )
    if (-not (Test-Path $Source)) {
        Write-Error @"
Release folder not found: $Source
Build all drops from repo root:
  python scripts/s2_build_release_bundles.py --profile all
Need orchestration for -InstallCore, full tree for -InstallFull.
"@
    }
    if (-not $SkipBackup -and (Test-Path $dst)) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $bak = "$dst.backup-$stamp"
        Write-Host "Backing up $dst -> $bak"
        Copy-Item -Recurse $dst $bak
    }
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Write-Host "Copying $Source -> $dst ($Label)"
    Copy-Item -Path (Join-Path $Source "*") -Destination $dst -Recurse -Force
    Write-Host "$Label install done." -ForegroundColor Green
}

if ($InstallFull) {
    Install-FaerieBundle -Source $fullSrc -Label "Full combined (orchestration + memory)"
}
elseif ($InstallCore) {
    Install-FaerieBundle -Source $orchSrc -Label "Core orchestration (OSS)"
}

if ($CollabEnv) {
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    if (-not $FaerieVaultShared) {
        $cand = Join-Path $FlowsearchRoot "ObsidianVault\00-SHARED"
        if (Test-Path $cand) { $FaerieVaultShared = $cand }
    }
    $cfg = @{
        faerie_project_root = $FaerieProjectRoot
        flowsearch_repo       = $FlowsearchRoot
        faerie_vault_shared   = $FaerieVaultShared
        claude_hooks_state    = $ClaudeHooksState
        vault_drops           = $VaultDrops
    }
    $writer = Join-Path $PSScriptRoot "Write-FaerieEnvFiles.ps1"
    & $writer -Config $cfg

    $launcher = Join-Path $PSScriptRoot "start-faerie-workstation.ps1"
    if (Test-Path $launcher) {
        Copy-Item $launcher (Join-Path $dst "start-faerie-workstation.ps1") -Force
        Write-Host "Installed $dst\start-faerie-workstation.ps1" -ForegroundColor Green
    }
}

if (-not $InstallCore -and -not $InstallFull -and -not $CollabEnv -and -not $Interactive) {
    Write-Host @"
faerie install - use -Interactive or specify modules:

  .\install-faerie.ps1 -Interactive

  .\install-faerie.ps1 -InstallCore          # OSS: orchestration only
  .\install-faerie.ps1 -InstallFull          # paid: full + memory (combined drop)
  .\install-faerie.ps1 -CollabEnv -FaerieProjectRoot "D:\path\to\project" ...

  Second window (queue mirror + dashboard):
    & `$env:USERPROFILE\.claude\start-faerie-workstation.ps1
"@
}

Write-Host ""
Write-Host "Syncthing: share ONLY ObsidianVault\00-SHARED - see ObsidianVault\START-COLLAB.md" -ForegroundColor Cyan
