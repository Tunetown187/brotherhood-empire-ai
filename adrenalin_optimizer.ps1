# AMD Adrenalin Optimizer Script
# Run as Administrator

# Registry paths for AMD Adrenalin settings
$AdrenalinRegPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"

# Function to set registry value
function Set-AdrenalinSetting {
    param(
        [string]$Path,
        [string]$Name,
        [string]$Value,
        [string]$Type = "String"
    )
    try {
        if (!(Test-Path $Path)) {
            New-Item -Path $Path -Force | Out-Null
        }
        Set-ItemProperty -Path $Path -Name $Name -Value $Value -Type $Type
        Write-Host "Successfully set $Name to $Value"
    }
    catch {
        Write-Host "Failed to set $Name : $_"
    }
}

# Set Performance Tuning
Write-Host "Configuring AMD Adrenalin Performance Settings..."

# Enable AMD Smart Access Memory if supported
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "KMD_EnableSmartAccessMemory" -Value "1" -Type "DWord"

# Optimize shader cache
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "ShaderCache" -Value "1" -Type "DWord"

# Set power mode to Performance
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "PP_PhmUseDynamicState" -Value "2" -Type "DWord"

# Enable hardware acceleration
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "EnableUlps" -Value "0" -Type "DWord"

# Configure Anti-Lag
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "KMD_AntiLag" -Value "1" -Type "DWord"

# Set texture filtering quality to Performance
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "TextureFilteringQuality" -Value "2" -Type "DWord"

# Set power limit to maximum
Set-AdrenalinSetting -Path $AdrenalinRegPath -Name "PP_PowerLimit" -Value "20" -Type "DWord"

Write-Host "`nOptimization complete. Please follow these manual steps in AMD Adrenalin Software:"
Write-Host "1. Open AMD Adrenalin Software"
Write-Host "2. Go to 'Performance' tab"
Write-Host "3. Enable 'AMD Smart Access Memory' if available"
Write-Host "4. Set 'Tuning Control' to 'Manual'"
Write-Host "5. Enable 'GPU Tuning'"
Write-Host "6. In 'Graphics' settings:"
Write-Host "   - Set 'Anti-Lag' to 'Enabled'"
Write-Host "   - Set 'Radeon Boost' to 'Disabled'"
Write-Host "   - Set 'Image Sharpening' to 'Disabled'"
Write-Host "   - Set 'Wait for Vertical Refresh' to 'Enhanced Sync'"
Write-Host "`nPlease restart your computer for all changes to take effect."
