# create_vault_junction.ps1 — Run as Administrator
# Part of faerie2 vault collaboration setup
#
# Creates a Directory Junction from the Syncthing staging folder to the
# vault's 00-SHARED\exchange\ directory so Syncthing can sync exchange/
# without touching private vault folders (01-PROTECTED\, 30-Evidence\, etc.).
#
# CUSTOMIZE the paths below before running if your vault is in a different location.
#
# Usage (PowerShell, run as Administrator):
#   .\create_vault_junction.ps1
#   .\create_vault_junction.ps1 -VaultRoot "E:\MyVault\CyberOps-UNIFIED"
#   .\create_vault_junction.ps1 -StagingDir "E:\Syncthing\CyberOps-collab"
#   .\create_vault_junction.ps1 -Remove

param(
    [string]$VaultRoot   = "D:\0LOCAL\0-ObsidianTransferring\CyberOps-UNIFIED",
    [string]$StagingDir  = "D:\0LOCAL\Syncthing\CyberOps-collab",
    [switch]$Remove
)

$ExchangeDir  = Join-Path $VaultRoot   "00-SHARED\exchange"
$JunctionPath = Join-Path $StagingDir  "exchange"

Write-Host ""
Write-Host "faerie2 Vault Junction Setup"
Write-Host ("=" * 50)
Write-Host "  Vault root:   $VaultRoot"
Write-Host "  Staging dir:  $StagingDir"
Write-Host "  Exchange dir: $ExchangeDir"
Write-Host "  Junction:     $JunctionPath"
Write-Host ""

# --- Remove mode ---
if ($Remove) {
    if (Test-Path $JunctionPath) {
        $item = Get-Item $JunctionPath -Force
        if ($item.LinkType -eq "Junction") {
            $item.Delete()
            Write-Host "  [OK] Junction removed: $JunctionPath"
        } else {
            Write-Host "  [WARN] $JunctionPath exists but is not a junction. Remove manually."
            exit 1
        }
    } else {
        Write-Host "  [INFO] Junction does not exist — nothing to remove."
    }
    exit 0
}

# --- Validate source ---
if (-not (Test-Path $ExchangeDir)) {
    Write-Host "  [ERROR] exchange/ dir not found: $ExchangeDir"
    Write-Host "  Run 0d_vault_collab_setup.py first to create the folder structure."
    exit 1
}

# --- Create staging dir if needed ---
if (-not (Test-Path $StagingDir)) {
    New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null
    Write-Host "  [OK] Created staging dir: $StagingDir"
}

# --- Handle existing junction ---
if (Test-Path $JunctionPath) {
    $item = Get-Item $JunctionPath -Force
    if ($item.LinkType -eq "Junction") {
        Write-Host "  [INFO] Junction already exists: $JunctionPath"
        Write-Host "         Target: $($item.Target)"
        Write-Host "  Nothing to do."
        exit 0
    } else {
        Write-Host "  [ERROR] $JunctionPath exists but is not a junction."
        Write-Host "  Remove it manually, then re-run this script."
        exit 1
    }
}

# --- Create junction ---
New-Item -ItemType Junction -Path $JunctionPath -Target $ExchangeDir | Out-Null

if (Test-Path $JunctionPath) {
    Write-Host "  [OK] Junction created:"
    Write-Host "       $JunctionPath -> $ExchangeDir"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Open Syncthing Web UI: http://localhost:8384"
    Write-Host "  2. Add folder: $StagingDir"
    Write-Host "     Folder ID: cyberops-collab-exchange"
    Write-Host "     Label:     CyberOps Collab Exchange"
    Write-Host "  3. Share the folder with your partner's device."
    Write-Host "  4. Partner accepts the share on their Syncthing instance."
    Write-Host ""
    Write-Host "  To verify: explorer.exe $StagingDir"
    Write-Host "             (exchange should appear as a shortcut/junction icon)"
} else {
    Write-Host "  [ERROR] Junction creation failed. Check that you are running as Administrator."
    exit 1
}
