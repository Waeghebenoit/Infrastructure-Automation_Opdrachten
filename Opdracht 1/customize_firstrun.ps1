$TextToInsert = @"
[connection]
id=Static_IP
uuid=2fcbd884-bc1f-4513-8f50-13e2d6ccc125
type=ethernet
interface-name=eth0

[ethernet]

[ipv4]
address1=192.168.88.2/24,192.168.88.1
dns=172.20.4.140;172.20.4.141;
method=manual

[ipv6]
addr-gen-mode=default
method=auto

[proxy]
"@
<#
$DriveLetter = "F:"  
$FilePath = "$DriveLetter\firstrun.sh"

# Check if the drive exists
if (Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -eq "$DriveLetter\" }) {
    # Check if the file exists at the specified path
    if (Test-Path -Path $FilePath) {
        Write-Output "File exists at: $FilePath"
    }
    else {
        Write-Output "File not found at: $FilePath"
    }
} 
else {
    Write-Output "Drive $DriveLetter not found."
}
#>


# Specify the file path
$FilePath = "C:\MCT - IoT Engineer\Infrastructure Automation\PS - opdracht 1\firstrun.sh"

# Read the content of the file into a variable
$FileContent = Get-Content -Path $FilePath -Raw

# Define the string to insert and the target text to search for
$TargetText = "rm -f /boot/firstrun.sh"

# Check if the target text exists and the insert text isn't already before it
$InsertPattern = [regex]::Escape("$TextToInsert`n$TargetText")
if ($FileContent -match [regex]::Escape($TargetText) -and -not ($FileContent -match $InsertPattern)) {
    # Insert the text before the target text
    $FileContent = $FileContent -replace [regex]::Escape($TargetText), "$TextToInsert`n$TargetText"
    Write-Output "Text inserted successfully."
}
else {
    Write-Output "Text already exists"
}

# Write the modified content back to the original file
Set-Content -Path $FilePath -Value $FileContent
