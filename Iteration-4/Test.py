import unittest
import time
import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy

def get_connected_devices():
    """Get connected Android devices."""
    devices = []
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True, check=True)
    lines = result.stdout.split("\n")[1:]
    devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]
    return devices

class AppiumTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not hasattr(cls, 'device_name') or cls.device_name is None:
            raise ValueError("device_name class attribute must be set before running tests.")
        
        cls.capabilities = {
            'platformName': 'Android',
            'automationName': 'uiautomator2',
            'deviceName': cls.device_name,
            'appPackage': 'com.android.settings',
            'appActivity': '.Settings',
            'language': 'en',
            'locale': 'US',
            'disableWindowAnimation': True,
        }

        appium_server_url = 'http://localhost:4723'
        cls.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(cls.capabilities))

    def find_and_act(self, by, value, action='click', text=None):
        """Find an element and perform an action."""
        element = self.driver.find_element(by=by, value=value)
        if action == 'click':
            element.click()
        elif action == 'send_keys':
            element.send_keys(text)
        else:
            raise ValueError(f"Unsupported action: {action}")

    def go_back(self, times=1):
        """Navigate back a specified number of times."""
        for _ in range(times):
            self.driver.back()

    def navigate_and_select(self, path, final_action='click', text=None):
        """Navigate through a series of UI elements and perform an action on the final element."""
        for step in path[:-1]:
            self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{step}")')
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().text("{path[-1]}")', action=final_action, text=text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class TestAppium(AppiumTestBase):
    def test_connection_settings(self):
        self.driver.implicitly_wait(10)  # Ensuring elements are loaded

        # Connection Settings
        self.navigate_and_select(["Connections", "Bluetooth"])
        self.navigate_and_select(["Connections", "NFC and contactless payments"])
        self.navigate_and_select(["Connections", "Wi-Fi"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Settings Button")
        self.navigate_and_select(["Connections", "View more"])

        # Navigating to MAC address type and selecting Phone MAC
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("MAC address type"))')
        self.navigate_and_select(["MAC address type", "Phone MAC"])

        self.go_back()  # Going back to previous screen

        # Advanced Settings and Hotspot 2.0
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="More options")
        self.navigate_and_select(["Connections", "Advanced settings"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiSelector().resourceId("android:id/switch_widget").instance(0)')
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Hotspot 2.0")

        self.go_back(3)  # Going back three screens

    def test_sounds_and_vibrations(self):
        # Mute system sounds via ADB command
        self.driver.execute_script("mobile: shell", {
            "command": "settings put system volume_system",
            "args": ["0"]
        })

        # Navigate to Sounds and vibration > Ringtone and select 80s Phone
        self.navigate_and_select(["Sounds and vibration", "Ringtone"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("80s Phone"))')
        
        self.go_back()  # Back to Sounds and vibration

        # Navigate to Notification sound and select Silent
        self.navigate_and_select(["Sounds and vibration", "Notification sound"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Silent"))')
        
        self.go_back()  # Back to Sounds and vibration

        # Navigate to System sound and toggle various switches
        self.navigate_and_select(["Sounds and vibration", "System sound"])
        switches = ["android:id/switch_widget.instance(1)", "android:id/switch_widget.instance(2)", 
                    "android:id/switch_widget.instance(3)", "android:id/switch_widget.instance(4)"]
        for switch in switches:
            self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value=f'new UiSelector().resourceId("{switch}")')

        self.go_back(2)  # Back to main settings menu

    def test_notifications_settings(self):
        self.driver.implicitly_wait(10)  # Ensure elements are loaded before interacting

        # Navigate to Notifications > App notifications
        self.navigate_and_select(["Notifications", "App notifications"])
        time.sleep(2)  # Pausing to ensure the UI is fully loaded
        
        # Toggle notification switches for various apps
        for instance in [0, 2, 4, 5, 6, 7, 8, 7, 8]:  # Specifying instances to interact with
            self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                            value=f'new UiSelector().resourceId("android:id/switch_widget").instance({instance})')

        self.go_back()  # Return to Notifications menu

        # Navigate to Notification pop-up style and select Apps to show as brief
        self.navigate_and_select(["Notifications", "Notification pop-up style"])
        self.navigate_and_select(["Notification pop-up style", "Apps to show as brief"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiSelector().resourceId("android:id/switch_widget").instance(0)')

        self.go_back(3)  # Return to the main settings menu

    def test_display_settings(self):
        self.driver.implicitly_wait(10)  # Ensure elements are loaded

        # Navigate to Display settings
        self.navigate_and_select(["Display"])

        # Navigate to Font size and style, then increase font size
        self.navigate_and_select(["Display", "Font size and style"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Increase font size")
        self.go_back()  # Back to Display settings

        # Navigate to Screen zoom and select the desired zoom level
        self.navigate_and_select(["Display", "Screen zoom"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="0")
        self.go_back()  # Back to Display settings

        # Navigate to and select Accidental touch protection
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                        value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Accidental touch protection"))')

        self.go_back()  # Return to the main settings menu

    def test_lockscreen_settings(self):
        # Ensure elements are loaded
        self.driver.implicitly_wait(10)

        # Navigate to Lock screen settings
        self.navigate_and_select(["Lock screen"])

        # Check if the screen lock type is already set to 'None'
        try:
            self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                    value='new UiSelector().resourceId("android:id/summary").text("None")')
            print("Screen lock type already set to 'None'. Skipping steps.")
            should_proceed = False
        except NoSuchElementException:
            print("Lock Screen Not set to None, Setting and Moving On.")
            should_proceed = True

        # Only proceed if the screen lock type is not "None"
        if should_proceed:
            self.navigate_and_select(["Lock screen", "Screen lock type", "None"])

        self.go_back(2)  # Return to the main settings menu

    def test_advanced_settings(self):
        # Ensure elements are loaded
        self.driver.implicitly_wait(10)

        # Navigate to Advanced Settings > Labs • Side key
        self.navigate_and_select(["Advanced Settings", "Labs  •  Side key"])

        # Toggle the Side key switch
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Side key")')
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("android:id/switch_widget")')

        self.go_back()  # Back to Advanced Settings

        # Enable Show toolbar after capturing for Screenshots
        self.navigate_and_select(["Advanced Settings", "Screenshots"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Show toolbar after capturing")

        self.go_back()  # Back to Advanced Settings

        # Navigate to Motions and gestures and toggle various switches
        self.navigate_and_select(["Advanced Settings", "Motions and gestures"])
        instances = [1, 2, 4, 5]  # Specifying switch instances to interact with
        for instance in instances:
            self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, 
                            value=f'new UiSelector().resourceId("android:id/switch_widget").instance({instance})')

        self.go_back()  # Back to Advanced Settings

        # Toggle settings for Show contacts when sharing content and Game Launcher
        self.navigate_and_select(["Advanced Settings", "Show contacts when sharing content"])
        self.navigate_and_select(["Advanced Settings", "Game Launcher"])

        self.go_back()  # Return to the main settings menu

    def test_apps_settings(self):
        # Navigate to Apps settings
        self.navigate_and_select(["Apps"])

        # Adjust default apps settings
        self.navigate_and_select(["Apps", "Default apps"])
        self.navigate_and_select(["Default apps", "Digital assistant app"])

        # Select the preferred device assistance app, then choose "None"
        self.navigate_and_select(["Digital assistant app", "Device assistance app"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("None")')

        # Properly manage back navigation to ensure we return to the main Apps menu
        self.go_back(4)

    def test_accessibility_settings(self):
        # Navigate to Accessibility settings
        self.navigate_and_select(["Accessibility"])
        time.sleep(1)  # Brief wait for settings to load

        # Retry logic for scrolling to a specific Accessibility setting
        for attempt in range(3):  # Allows up to three attempts
            try:
                self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                value='new UiScrollable(new UiSelector().scrollable(true)).setMaxSearchSwipes(100).scrollIntoView(new UiSelector().text("Accessibility"))',
                                action='click')
                print(f"Attempt {attempt + 1}: Accessibility option found and selected.")
                attempt_success = True
                break
            except NoSuchElementException:
                print(f"Attempt {attempt + 1} failed to find 'Accessibility'. Retrying...")
                if attempt < 2:  # Avoid sleeping on the last attempt
                    time.sleep(1)

        if not attempt_success:
            print("Failed to find 'Accessibility' after 3 attempts.")
            return  # Exit the test early if unable to find the Accessibility option

        # Navigate and interact within the Accessibility settings
        self.navigate_and_select(["Accessibility", "Interaction and dexterity", "Touch and hold delay"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Medium (1 second)")

        self.go_back(2)  # Return to Accessibility main page

        # Additional Accessibility settings interactions
        self.navigate_and_select(["Accessibility", "Visibility enhancements"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("android:id/switch_widget").instance(4)')

        self.go_back()  # Return to Accessibility main page

        self.navigate_and_select(["Accessibility", "Installed apps", "Remote Control"])
        self.find_and_act(by=AppiumBy.ACCESSIBILITY_ID, value="Off")
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().resourceId("android:id/button1")')

        self.go_back(4)  # Return to the main settings menu

    def test_software_update_and_dev_options(self):
        # Ensure elements are loaded
        self.driver.implicitly_wait(10)

        # Navigate to and activate Auto download over Wi-Fi in Software Update settings
        self.navigate_and_select(["Settings", "Software update"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("Auto download over Wi-Fi")', action='click')

        # Navigate to Developer options and turn it on
        self.navigate_and_select(["Settings", "Developer options"])
        self.find_and_act(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("On")', action='click')

if __name__ == '__main__':
    devices = get_connected_devices()
    for device in devices:
        TestAppium.device_name = device
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)
        print(f"Running tests on device: {device}")
        unittest.TextTestRunner().run(suite)