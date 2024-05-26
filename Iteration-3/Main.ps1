# List all device serial numbers and store them in an array
$devices = adb devices | Select-String 'device$' | ForEach-Object { $_.Line.Split()[0] }

function SetPreliminarySettings {
    param (
        [string]$device
    )
    # Brightness and Orientation and Wake up
    adb shell input keyevent KEYCODE_WAKEUP
    adb shell input swipe 500 1500 500 500
    adb -s $device shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
    adb -s $device shell settings put system user_rotation 0
    adb -s $device shell settings put system screen_brightness 255
    adb -s $device shell settings put system screen_brightness_mode 0
}

function SetConnectivitySettings {
    param (
        [string]$device
    )
    # Disable Advanced Wifi Settings
    python find.py $device "Connections > Wi-Fi"
    adb -s $device shell settings put global wifi_networks_available_notification_on 0
        Start-Sleep -Seconds 2
    adb -s $device shell input tap 1045 250
        Start-Sleep -Seconds 2
    adb -s $device shell input tap 875 480
        Start-Sleep -Seconds 2
    python find.py $device "Start Here > Hotspot 2.0 > On"
        Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
    
    # Disable Basic Connectivity
    python find.py $device "Connections > Bluetooth > On"
        Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
    python find.py $device "Connections > NFC and contactless payments > On"
        Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
}

function SetGeneralSettings {
    param (
        [string]$device
    )
    # Sounds
    python find.py $device "Sounds and vibration > Ringtone > 80s Phone"
    adb -s $device shell settings put system notification_sound "Silent"
    Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS

    python find.py $device "Sounds and vibration > System sound > Touch interactions > Dialing keypad > Samsung Keyboard > Charging > Screen lock/unlock"
    adb -s $device shell input tap 195 450
    Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
}
function DisableAppNotifications {
    param (
        [string]$device
    )
    # List of apps to revoke notifications permission
    $apps = @(
        "com.samsung.android.themestore",
        "com.google.android.gms",
        "com.android.vending",
        "com.samsung.android.messaging",
        "com.google.android.apps.messaging",
        "com.samsung.vvm",
        "com.sec.android.daemonapp",
        "com.google.android.googlequicksearchbox",
        "com.sec.android.app.sbrowser"
    ) #"com.samsung.android.themecenter",

    foreach ($app in $apps) {
        adb -s $device shell pm revoke $app android.permission.POST_NOTIFICATIONS
    }

    # Assuming the screen resolution and UI layout, this may need adjustment
    adb -s $device shell input tap 500 2200
    Start-Sleep -Seconds 2
    python find.py $device "Notifications > Notification pop-up style > Apps to show as brief > All apps"
    Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS

    #Lock Screen Notifs
    python find.py $device "Notifications > Lock screen notifications > On"
}

function ConfigureDeviceSettings {
    param (
        [string]$device
    )
    
    # Zoom
    adb -s $device shell wm density 420
    
    # Font
    adb -s $device shell settings put system font_scale 1.15
    
    # Touch Protection
    python find.py $device "Display > Accidental touch protection"
    Start-Sleep -Seconds 1; adb -s $device shell am start -a android.settings.SETTINGS
    
    # Disable the Lockscreen
    adb -s $device shell locksettings set-disabled true
    
    # Advanced Features
    python find.py $device "Advanced features > Show contacts when sharing content > Game Launcher > Screenshots > Show toolbar after capturing > On"
    Start-Sleep -Seconds 1; adb -s $device shell am start -a android.settings.SETTINGS
    python find.py $device "Advanced features > Motions and gestures > Double tap to turn on screen > Double tap to turn off screen > Turn over to mute > Pick up phone to call"
    Start-Sleep -Seconds 1; adb -s $device shell am start -a android.settings.SETTINGS
    python find.py $device "Advanced features > Side key > Double press"
    
    # App Permissions
    python find.py $device "Apps > Choose default apps > Digital assistant app > Google > None"
    Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
    python find.py $device "Apps > GSI Phone > Permissions > Microphone > Allow only while using the app"
    Start-Sleep -Seconds 2; adb -s $device shell am start -a android.settings.SETTINGS
    python find.py $device "Apps > GSI Phone > Permissions > Notifications > Allow notifications > Badge > Pop-up"

    #Remove Animations
    adb shell settings put global window_animation_scale 0
    adb shell settings put global transition_animation_scale 0
    adb shell settings put global animator_duration_scale 0

    #Acessability
    python find.py $device "Accessibility > Interaction and dexterity > Touch and hold delay > Medium (1 second)"
    python find.py $device "Accessibility > Installed apps > Remote Control > Off > Allow"
    
    # Updates
    python find.py $device "Software update > Auto download over Wi-Fi"
}

function LaunchRemoteControlAgent {
    param (
        [string]$device
    )
    adb -s $device shell monkey -p com.springdel.rc.agent.dpc 1
    Start-Sleep -Seconds 2
    adb -s $device shell input tap 545 490 # Start Sharing
    Start-Sleep -Seconds 2
    adb -s $device shell input keyevent KEYCODE_HOME
}

function LaunchGSIPhoneApp {
    param (
        [string]$device
    )
    adb -s $device shell monkey -p com.hsh.gsiphone 1
    Start-Sleep -Seconds 2
    adb -s $device shell input tap 780 1300
    Start-Sleep -Seconds 2
    adb shell input swipe 540 2398 540 1978
    Start-Sleep -Seconds 2
    adb -s $device shell input tap 580 2100
    Start-Sleep -Seconds 2
    adb -s $device shell input keyevent KEYCODE_HOME
    Start-Sleep -Seconds 2
}

function LaunchSpringmaticApp {
    param (
        [string]$device
    )
    adb -s $device shell monkey -p com.springdel.android.dpc 1
    Start-Sleep -Seconds 2
    adb -s $device shell input tap 580 1200
    Start-Sleep -Seconds 2
    adb -s $device shell input keyevent KEYCODE_HOME
    Start-Sleep -Seconds 2
}

function Main {
    param (
        [string]$device
    )
    SetPreliminarySettings -device $device
    SetConnectivitySettings -device $device
    SetGeneralSettings -device $device
    DisableAppNotifications -device $device
    ConfigureDeviceSettings -device $device
    LaunchRemoteControlAgent -device $device
    LaunchGSIPhoneApp -device $device
    LaunchSpringmaticApp -device $device
}

# Loop through all connected devices
foreach ($device in $devices) {
    Write-Host "Running commands on device $device"
    Main -device $device
}