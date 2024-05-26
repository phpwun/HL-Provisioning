import unittest
import time
import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def get_connected_devices():
    
    """Get connected Android devices."""
    devices = []
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True, check=True)
    lines = result.stdout.splitlines()
    for line in lines[1:]:
        if "\tdevice" in line:
            device_id = line.split("\t")[0]
            devices.append(device_id)
    return devices


class TestAppium(unittest.TestCase):
    device_name = None  # Placeholder for device name

    @classmethod
    def setUpClass(cls):
        super(TestAppium, cls).setUpClass()
        if cls.device_name is None:
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

    @classmethod

    def go_back(self):
      self.driver.back()

    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()
        super().tearDownClass()

    def test_find_battery(self):
        self.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        #Connection Settings
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Connections")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().description("Bluetooth")')
        el.click()

        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().description("NFC and contactless payments")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Wi-Fi")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="Settings Button")
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("View more")')
        el.click()
        
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("MAC address type"))')
        element.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Phone MAC")')
        el.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="More options")
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Advanced settings")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(0)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="Hotspot 2.0")
        el.click()
        
        self.go_back()
        self.go_back()
        self.go_back()
        

        #Sounds and Such

        self.driver.execute_script("mobile: shell", {
            "command": "settings put system volume_system",
            "args": ["0"]
        })

        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Sounds and vibration")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Ringtone")')
        el.click()
        
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("80s Phone"))')
        element.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Notification sound")')
        el.click()
        
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Silent"))')
        element.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("System sound")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(1)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(2)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(3)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(4)')
        el.click()
        
        self.go_back()
        self.go_back()
        

        #Notifications
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Notifications")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("App notifications")')
        el.click()
        time.sleep(2)
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(0)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(2)')
        el.click()

        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(4)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(5)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(6)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(7)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(8)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(7)')
        el.click()
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(8)')
        el.click()

        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Notification pop-up style")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Apps to show as brief")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(0)')
        el.click()
        
        self.go_back()
        self.go_back()
        self.go_back()
        

        #Display
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Display"))')
        element.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Font size and style")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="Increase font size")
        el.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Screen zoom")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="0")
        el.click()
        
        self.go_back()

        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Accidental touch protection"))')
        element.click()

        self.go_back()
        

        #Lockscreen
        # Navigate to the "Lock screen" section
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                          value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Lock screen"))')
        element.click()
        try:
            summary_element = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().resourceId("android:id/summary").text("None")')
            # If the above line does not raise an exception, it means "None" is found
            print("Screen lock type already set to 'None'. Skipping steps.")
            should_proceed = False
        except:
            print("Lock Screen Not set to None, Setting and Moving On.")
            should_proceed = True

        # Only proceed if the screen lock type is not "None"
        if should_proceed:
            # Click on "Screen lock type"
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().text("Screen lock type")')
            el.click()
            
            # Select "None" as the screen lock type
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().text("None")')
            el.click()

        self.go_back()
        self.go_back()

        #Advanced Settings
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Labs  •  Side key"))')
        element.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Side key")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget")')
        el.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Screenshots")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ACCESSIBILITY_ID,
              value="Show toolbar after capturing")
        el.click()
        
        self.go_back()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Motions and gestures")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(1)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(2)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(4)')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("android:id/switch_widget").instance(5)')
        el.click()
        
        self.go_back()

        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Show contacts when sharing content")')
        el.click()

        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Game Launcher")')
        el.click()

        self.go_back()
        

        #Apps
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Apps"))')
        element.click()
        time.sleep(1)
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().resourceId("com.android.settings:id/default_app_settings_title")')
        el.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Digital assistant app")')
        el.click()
        time.sleep(1)
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Device assistance app").instance(1)')
        el.click()
        time.sleep(1)
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("None")')
        el.click()
        time.sleep(1)
        self.go_back()
        self.go_back()
        self.go_back()
        self.go_back()
        
        # Accessibility
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Accessibility"))')
        element.click()
        time.sleep(1)
        attempt_success = False

        for attempt in range(3):  # Two attempts
            try:
                print("Attempt to scroll to the 'Accessibility' option and click it")
                element = self.driver.find_element(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiScrollable(new UiSelector().scrollable(true)).setMaxSearchSwipes(100).scrollIntoView(new UiSelector().text("Accessibility"))'
                )
                element.click()
                attempt_success = True  # If the click succeeds, set this flag to True
                break  # Break out of the loop on success
            except NoSuchElementException:
                print(f"Attempt {attempt + 1} failed to find 'Accessibility'. Retrying...")
                if attempt == 0:  # Only print this if it's going to try again
                    print("Retrying...")

        if not attempt_success:
            print("Failed to find 'Accessibility' after 2 attempts.")
        else:
            # If the 'Accessibility' option was successfully clicked, proceed with the following commands
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().text("Interaction and dexterity")')
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                value='new UiSelector().text("Touch and hold delay")')
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ACCESSIBILITY_ID,
                value="Medium (1 second)")
            el.click()
            
            # Presuming `self.go_back()` is a defined method that navigates back a screen
            self.go_back()
            self.go_back()

            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                  value='new UiSelector().text("Visibility enhancements")')
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                  value='new UiSelector().resourceId("android:id/switch_widget").instance(4)')
            el.click()
            
            self.go_back()
            
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                  value='new UiSelector().text("Installed apps")')
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                  value='new UiSelector().text("Remote Control")')
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ACCESSIBILITY_ID,
                  value="Off")
            el.click()
            
            el = self.driver.find_element(
                by=AppiumBy.ANDROID_UIAUTOMATOR,
                  value='new UiSelector().resourceId("android:id/button1")')
            el.click()
            
            self.go_back()
            self.go_back()
            self.go_back()
            self.go_back()

        #Software Update
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Software update"))')
        element.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("Auto download over Wi-Fi")')
        el.click()

        #Dev Options
        element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Developer options"))')
        element.click()
        
        el = self.driver.find_element(
            by=AppiumBy.ANDROID_UIAUTOMATOR,
              value='new UiSelector().text("On")')
        el.click()
        
        pass

# Example usage
if __name__ == '__main__':
    devices = get_connected_devices()
    for device in devices:
        # Set the device_name attribute for the class before running tests
        TestAppium.device_name = device
        # Dynamically create a test suite containing all tests from TestAppium
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)
        print(f"Running tests on device: {device}")
        unittest.TextTestRunner().run(suite)