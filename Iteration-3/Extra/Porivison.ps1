#Potrait Fix
adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
adb shell settings put system user_rotation 0

# Disable Bluetooth
adb shell settings put global bluetooth_on 0

# Disable NFC and contactless payments
adb shell settings put global nfc_on 0

# Configure Wi-Fi Advanced Settings
adb shell settings put global wifi_networks_available_notification_on 0
adb shell settings put global wifi_hotspot2_enabled 0

# Set custom ringtone (80s_phone) for calls
adb shell settings put system ringtone "content://settings/system/ringtone/80s_phone"

# Silence notification sounds
adb shell settings put system notification_sound "Silent"

# Mute system volume
adb shell settings put system volume_system 0

# Disable sound effects
adb shell settings put system sound_effects_enabled 0

# Enable app notification settings
adb shell settings put global app_notification_settings_enabled 1

# Set app notification priority to lowest
adb shell settings put global app_notification_settings 0

# Hide notifications on the lock screen
adb shell settings put global lock_screen_show_notifications 0

# Disable heads-up notifications
adb shell settings put global heads_up_notifications_enabled 0

# Hide specific notification icons (use "notification_icon_list" as a placeholder)
adb shell settings put global icon_blacklist "notification_icon_list"

# Disable floating notifications
adb shell settings put global floating_notifications_enabled 0

# Adjust screen brightness to maximum (255)
adb shell settings put system screen_brightness 255

# Disable automatic screen brightness adjustment
adb shell settings put system screen_brightness_mode 0

# Increase font scale by 15% (1.15)
adb shell settings put system font_scale 1.15

# Set display density to 320 DPI
   #adb shell wm density 320

# Set screen timeout to 60 seconds
adb shell settings put system screen_off_timeout 60000

# Disable edge panels
adb shell settings put secure edge_panels_enabled 0

# Hide pointer location overlay
adb shell settings put system pointer_location 0

# Disable touch exploration
adb shell settings put secure touch_exploration_enabled 0

# Disable lock screen
adb shell settings put secure lockscreen.disabled 1

# Disable advanced features related to side key
adb shell settings put secure side_key_settings 0

# Enable double-tap to wake
adb shell settings put secure double_tap_to_wake 1

# Enable double-tap to sleep
adb shell settings put secure double_tap_to_sleep 1

# Disable motion gestures
adb shell settings put secure motion_gesture_settings 0

# Disable screenshot toolbar
adb shell settings put secure screenshot_toolbar_enabled 0

#Animations
adb shell settings put global transition_animation_scale 0
adb shell settings put global window_animation_scale 0
adb shell settings put global animator_duration_scale 0

# Default Apps (Set to NONE)
adb shell settings put secure assist_structure "None"