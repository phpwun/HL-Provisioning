# Preliminary
    
    #Brightness and Orientation 
        adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
        adb shell settings put system user_rotation 0
        adb shell settings put system screen_brightness 255
        adb shell settings put system screen_brightness_mode 0

#Connectivity

    # Disable Advanced Wifi Settings 
        python find.py "Connections > Wi-Fi"
        adb shell settings put global wifi_networks_available_notification_on 0
        adb shell input tap 1045 250
            Start-Sleep(1)
        adb shell input tap 875 480
        python find.py "Start Here > Hotspot 2.0 > On"
            Start-Sleep -Seconds 2; adb shell am start -a android.settings.SETTINGS
    
    #Disable Basic Connectivity 
        python find.py "Connections > Bluetooth > On"
            Start-Sleep -Seconds 2; adb shell am start -a android.settings.SETTINGS

        python find.py "Connections > NFC and contactless payments > On"
            Start-Sleep -Seconds 2; adb shell am start -a android.settings.SETTINGS

#General Settings
    
    #Sounds
        python find.py "Sounds and vibration > Ringtone > 80s Phone"
            Start-Sleep -Seconds 2; adb shell am start -a android.settings.SETTINGS

        adb shell settings put system notification_sound "Silent"
            Start-Sleep -Seconds 2; adb shell am start -a 

        python find.py "Sounds and vibration > System sound > Touch interactions > Dialing keypad > Samsung Keyboard > Charging > Screen lock/unlock"
            adb shell input tap 195 450


# Turn of Specific App Notifications
    adb shell pm revoke com.samsung.android.themestore android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.samsung.android.themecenter android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.google.android.gms android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.android.vending android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.samsung.android.messaging android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.google.android.apps.messaging android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.samsung.vvm android.permission.POST_NOTIFICATIONS
    adb shell pm revoke com.sec.android.daemonapp android.permission.POST_NOTIFICATIONS

#Breif Notifications
    adb shell input tap 500 2200; Start-Sleep -Seconds 2
        python find.py "Notifications > Notification pop-up style > Apps to show as brief > All apps"

# Notification Pop up style 

# Lock Screen Notifications

adb shell wm density 420

adb shell settings put system font_scale 1.15

# Touch Protection

adb shell locksettings set-disabled true

# Advanced Featuees

#Apps Default Apps

# Accessibility 

adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0


