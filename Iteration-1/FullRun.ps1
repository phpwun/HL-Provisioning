# Fix Orientation
adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
adb shell settings put system user_rotation 0

adb shell settings put system screen_brightness 255

adb shell settings put system screen_brightness_mode 0

python find.py "Connections > Wi-Fi"

adb shell am start -a android.settings.SETTINGS

adb shell input tap 945 250  # More Options

adb shell input tap 875 480  # Advanced Options

adb shell settings put global wifi_networks_available_notification_on 0

python find.py "Start Here > Hotspot 2.0 > On"

adb shell am start -a android.settings.SETTINGS

python find.py "Connections > Bluetooth > On"

adb shell am start -a android.settings.SETTINGS

python find.py "Connections > NFC and contactless payments > On"

adb shell am start -a android.settings.SETTINGS

python find.py "Sounds and vibration > Ringtone > 80s Phone"

adb shell am start -a android.settings.SETTINGS

adb shell settings put system notification_sound "Silent"

adb shell am start -a android.settings.SETTINGS

# Make System Sound Path and Toggles

# Make App Notifications Turn off Toggles

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


