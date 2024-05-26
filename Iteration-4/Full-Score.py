import unittest
import time
import subprocess
import logging
import signal
import requests
import sys
from appium import webdriver
from concurrent.futures import ThreadPoolExecutor, as_completed
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from threading import Thread

# Define constants
APPIUM_SERVER_DEFAULT_PORT = 4723
SERVER_CHECK_DELAY = 2
SERVER_CHECK_RETRIES = 5
APPIUM_COMMAND_PATH = "C:\\Users\\aritt\\AppData\\Roaming\\npm\\appium.cmd"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

appium_processes = []

def is_appium_server_running(port, retries=SERVER_CHECK_RETRIES, delay=SERVER_CHECK_DELAY):
    """Check if Appium server is running by polling the /status endpoint with retries."""
    for attempt in range(retries):
        try:
            response = requests.get(f"http://localhost:{port}/status")
            if response.status_code == 200:
                logging.info(f"Server running on port {port}: Status code 200 received on attempt {attempt + 1}")
                return True
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} of {retries}: Error checking Appium server status on port {port}: {e}")
        time.sleep(delay)
    return False


def signal_handler(sig, frame):
    logging.info('Shutting down gracefully...')
    for proc in appium_processes:
        logging.info(f"Terminating Appium server on port {proc['port']}")
        proc['process'].terminate()
        try:
            proc['process'].wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc['process'].kill()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_connected_devices():
    logging.info("Checking for connected Android devices...")
    devices = []
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, text=True, check=True)
    lines = result.stdout.splitlines()
    for line in lines[1:]:
        if "\tdevice" in line:
            device_id = line.split("\t")[0]
            devices.append(device_id)
    if devices:
        logging.info(f"Connected devices: {devices}")
    else:
        logging.warning("No devices connected. Please connect a device and try again.")
        sys.exit(1)
    return devices

def start_appium_server(port):
    logging.info(f"Attempting to start Appium server on port {port}...")
    try:
        # Start the Appium server using a subprocess
        log_file = open(f'appium_{port}.log', 'a')
        process = subprocess.Popen([APPIUM_COMMAND_PATH, "-p", str(port)], stdout=log_file, stderr=subprocess.STDOUT)
        # Wait for the server to start
        time.sleep(5)

        # Check if the server is running
        if is_appium_server_running(port):
            logging.info(f"Appium server started successfully on port {port}.")
            appium_processes.append({'port': port, 'process': process})
            return True  # Indicates the server started successfully
        else:
            logging.error(f"Failed to start Appium server on port {port}.")
            process.terminate()
            return False
    except Exception as e:
        logging.error(f"Exception occurred while starting Appium server: {e}")
        return False

class TestAppium(unittest.TestCase):
    device_name = None  # Placeholder for device name
    appium_port = None  # Placeholder for Appium port

    @classmethod
    def setUpClass(cls):
        super(TestAppium, cls).setUpClass()
        if cls.device_name is None or cls.appium_port is None:
            raise ValueError("Both device_name and appium_port class attributes must be set before running tests.")

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

        appium_server_url = f'http://localhost:{cls.appium_port}'
        cls.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(cls.capabilities))

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()
        super(TestAppium, cls).tearDownClass()

    def go_back(self):
        self.driver.back()

    def test_find_battery(self):
        logging.info("Starting test: test_find_battery")
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

        #element = self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
        #                                    value='new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Accidental touch protection"))')
        #element.click()

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
        

        #Accessability
        attempt_success = False

        for attempt in range(3):  # Two attempts
            try:
                # Attempt to scroll to the "Accessibility" option and click it
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
        logging.info("Finished test: test_find_battery")
        pass


def run_tests_on_device(device_id, port):
    def test_runner():
        logging.info(f"Running tests on device: {device_id} on port {port}")
        TestAppium.device_name = device_id
        TestAppium.appium_port = port
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAppium)
        unittest.TextTestRunner().run(suite)
    
    # Start each test suite in its own thread
    test_thread = Thread(target=test_runner)
    test_thread.start()
    return test_thread

def main():
    print("main")
    devices = get_connected_devices()  # Get the list of connected devices
    if not devices:
        logging.error("No devices connected. Exiting.")
        return

    starting_port = 4723
    threads = []
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        future_to_port = {executor.submit(start_appium_server, starting_port + i): starting_port + i for i, _ in enumerate(devices)}
        future_to_device = {future: devices[i] for i, future in enumerate(future_to_port)}

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            device_id = future_to_device[future]
            try:
                result = future.result()
                if result:
                    logging.info(f"Server successfully started on port {port}.")
                    # Run tests on the device associated with this server in a non-blocking manner
                    test_thread = run_tests_on_device(device_id, port)
                    threads.append(test_thread)
                else:
                    logging.error(f"Failed to start server on port {port}.")
            except Exception as exc:
                logging.error(f"Server start generated an exception: {exc}")

    # Wait for all test threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()