# GPU Optimization Script
# Run as administrator for full functionality

# Set high performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Function to set app GPU preference
function Set-AppGPUPreference {
    param(
        [string]$AppPath,
        [string]$PreferenceValue = "2" # 2 = High Performance
    )
    
    $RegistryPath = "HKCU:\Software\Microsoft\DirectX\UserGpuPreferences"
    if (!(Test-Path $RegistryPath)) {
        New-Item -Path $RegistryPath -Force
    }
    
    Set-ItemProperty -Path $RegistryPath -Name $AppPath -Value "GpuPreference=$PreferenceValue;"
}

# List of apps to optimize
$appsToOptimize = @(
    "${env:ProgramFiles}\Mozilla Firefox\firefox.exe",
    "${env:LocalAppData}\Programs\Opera\opera.exe",
    "${env:LocalAppData}\Discord\app-1.0.9027\Discord.exe"
)

# Set GPU preference for each app
foreach ($app in $appsToOptimize) {
    if (Test-Path $app) {
        Set-AppGPUPreference -AppPath $app
        Write-Host "Optimized GPU settings for: $app"
    }
}

# Configure AMD-specific settings via registry
$AMDRegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
if (Test-Path $AMDRegPath) {
    # Enable hardware acceleration
    Set-ItemProperty -Path $AMDRegPath -Name "KMD_EnableComputePreemption" -Value 1
    
    # Optimize for performance
    Set-ItemProperty -Path $AMDRegPath -Name "PP_GPUPowerDownEnabled" -Value 1
    Set-ItemProperty -Path $AMDRegPath -Name "PP_ThermalAutoThrottlingEnable" -Value 1
}

Write-Host "GPU optimization complete. Please restart your computer for changes to take effect."
