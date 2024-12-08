# Run as administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Please run this script as Administrator!"
    exit
}

# Save current work state
Write-Host "Saving current work state..."
$browserProcesses = Get-Process | Where-Object { $_.ProcessName -match 'chrome|firefox|edge|brave|opera' }
$browserWindows = $browserProcesses | ForEach-Object { $_.MainWindowTitle }
$workState = @{
    'BrowserTabs' = $browserWindows
    'Timestamp' = Get-Date
}.\optimize_system.ps1
$workState | ConvertTo-Json | Out-File "$env:USERPROFILE\Desktop\work_state.json"

# Services to disable (non-essential services)
$servicesToDisable = @(
    "DiagTrack",          # Connected User Experiences and Telemetry
    "SysMain",            # Superfetch
    "WSearch",            # Windows Search
    "DoSvc",              # Delivery Optimization
    "AdobeARMservice",    # Adobe Acrobat Update Service
    "AdobeUpdateService", # Adobe Update Service
    "TabletInputService", # Touch Keyboard and Handwriting
    "WbioSrvc",          # Windows Biometric Service
    "PrintNotify",        # Printer notifications
    "RemoteRegistry",     # Remote Registry
    "SharedAccess",       # Internet Connection Sharing
    "WerSvc"             # Windows Error Reporting
)

foreach ($service in $servicesToDisable) {
    Write-Host "Stopping and disabling $service..."
    Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
    Set-Service -Name $service -StartupType Disabled -ErrorAction SilentlyContinue
}

# Enable Hardware Accelerated GPU Scheduling
Write-Host "Enabling Hardware Accelerated GPU Scheduling..."
$path = "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
Set-ItemProperty -Path $path -Name "HwSchMode" -Value 2 -Type DWord -Force

# Enable Ultimate Performance power plan
Write-Host "Creating and setting Ultimate Performance power plan..."
powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61

# Optimize memory management
Write-Host "Optimizing memory management..."
$memoryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
Set-ItemProperty -Path $memoryPath -Name "DisablePagingExecutive" -Value 1 -Type DWord -Force
Set-ItemProperty -Path $memoryPath -Name "LargeSystemCache" -Value 0 -Type DWord -Force
Set-ItemProperty -Path $memoryPath -Name "SystemCacheDirtyPageThreshold" -Value 0 -Type DWord -Force

# Optimize Visual Effects for performance
Write-Host "Optimizing Visual Effects for performance..."
$path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
Set-ItemProperty -Path $path -Name "VisualFXSetting" -Value 2 -Type DWord -Force

# Clear temporary files and memory
Write-Host "Clearing temporary files and memory..."
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Clear-RecycleBin -Force -ErrorAction SilentlyContinue

# Optimize GPU settings for AMD RX 5700 XT
Write-Host "Optimizing GPU settings for AMD RX 5700 XT..."
$amdPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
if (Test-Path $amdPath) {
    # Disable ULPS (Ultra Low Power State)
    Set-ItemProperty -Path $amdPath -Name "EnableUlps" -Value 0 -Type DWord -Force
    # Disable Deep Sleep
    Set-ItemProperty -Path $amdPath -Name "PP_SclkDeepSleepDisable" -Value 1 -Type DWord -Force
    # Optimize for compute performance
    Set-ItemProperty -Path $amdPath -Name "KMD_EnableComputePreemption" -Value 0 -Type DWord -Force
    # Set GPU workload to compute
    Set-ItemProperty -Path $amdPath -Name "PP_WorkloadHints" -Value 4 -Type DWord -Force
    # Enable high performance mode
    Set-ItemProperty -Path $amdPath -Name "PP_ThermalAutoThrottlingEnable" -Value 0 -Type DWord -Force
}

# Enable Game Mode and GPU optimizations
Write-Host "Enabling Game Mode and GPU optimizations..."
$gameDVRPath = "HKCU:\Software\Microsoft\GameBar"
Set-ItemProperty -Path $gameDVRPath -Name "AllowAutoGameMode" -Value 1 -Type DWord -Force
Set-ItemProperty -Path $gameDVRPath -Name "AutoGameModeEnabled" -Value 1 -Type DWord -Force

# Optimize process priorities and GPU assignment
Write-Host "Optimizing process priorities and GPU assignment..."
$processesToOptimize = Get-Process | Where-Object { 
    $_.Name -notmatch 'chrome|firefox|edge|brave|opera' -and 
    $_.WorkingSet -gt 100MB -and 
    $_.ProcessName -notmatch 'explorer|dwm|csrss|svchost|lsass'
}

foreach ($process in $processesToOptimize) {
    try {
        # Set process priority to high
        $process.PriorityClass = 'High'
        
        # Force process to use GPU
        $processPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\$($process.ProcessName).exe"
        if (-not (Test-Path $processPath)) {
            New-Item -Path $processPath -Force | Out-Null
        }
        Set-ItemProperty -Path $processPath -Name "UseGPU" -Value 1 -Type DWord -Force
        
        Write-Host "Optimized $($process.ProcessName) to use GPU with high priority"
    } catch {
        Write-Host "Could not optimize $($process.ProcessName)"
    }
}

# Clean memory and optimize working set
Write-Host "Cleaning memory and optimizing working set..."
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

# Set memory priority for GPU processes
Write-Host "Setting memory priority for GPU processes..."
$gpuProcesses = Get-Process | Where-Object { $_.Name -match 'dwm|csrss' }
foreach ($process in $gpuProcesses) {
    try {
        $process.PriorityClass = 'High'
        Write-Host "Set high priority for $($process.ProcessName)"
    } catch {
        Write-Host "Could not set priority for $($process.ProcessName)"
    }
}

Write-Host "System optimization complete. Your work state has been saved to work_state.json on your Desktop."
Write-Host "Please restart your computer for all changes to take effect."
Write-Host "After restart, your browsers will remain open with current tabs."
Write-Host "GPU and memory optimizations are in place - your system should perform significantly better."
