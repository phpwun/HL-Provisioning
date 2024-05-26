Write-Output "Starting device monitor and test runner..."

function Get-UniquePort {
    # Example function to generate a unique port number
    # In practice, you might want to manage port numbers more systematically
    $global:LastPort += 1
    return $global:LastPort
}

$global:LastPort = 4723  # Initial port for Appium servers

function Start-AppiumServerForDevice {
    param (
        [string]$DeviceID,
        [int]$AppiumPort
    )
    $AppiumCmd = "appium"
    $AppiumArgs = "-p $AppiumPort"
    Write-Output "Starting Appium server for device $DeviceID on port $AppiumPort..."
    
    # Using Start-Process with -ArgumentList
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $AppiumCmd, $AppiumArgs -NoNewWindow -Wait
    Write-Output "Appium server started."
}

function Run-TestsForDevice {
    param (
        [string]$DeviceID,
        [int]$AppiumPort
    )
    Write-Output "Running tests on device $DeviceID using Appium server on port $AppiumPort..."
    $cmd = "python.exe"
    $ServrArgs = "C:\Users\aritt\Documents\Work\Peninsula\Main-Copy.py", "--device_name", $DeviceID, "--appium_server_url", "http://localhost:$AppiumPort"
    & $cmd $ServrArgs
}

function Monitor-ConnectedDevices {
    $ConnectedDevices = @{}
    $MaxServers = 8

    while ($true) {
        $currentDevices = adb devices | Where-Object { $_ -match "device$" } | ForEach-Object { ($_ -split "\t")[0] }

        foreach ($device in $currentDevices) {
            if (-not $ConnectedDevices.ContainsKey($device) -and $ConnectedDevices.Count -lt $MaxServers) {
                $port = Get-UniquePort
                Start-AppiumServerForDevice -DeviceID $device -AppiumPort $port
                $ConnectedDevices.Add($device, $port)
                Run-TestsForDevice -DeviceID $device -AppiumPort $port
            }
        }

        # Check for disconnected devices and remove them from the tracking dictionary
        $ConnectedDevices.Keys | Where-Object { $_ -notin $currentDevices } | ForEach-Object {
            $ConnectedDevices.Remove($_)
        }

        Start-Sleep -Seconds 5  # Adjust the sleep time as needed
    }
}

try {
    Monitor-ConnectedDevices
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}