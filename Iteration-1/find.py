import uiautomator2 as u2
import time
import subprocess
import sys

# Connect to the device
d = u2.connect()

def start_settings_app():
    """
    Start the settings app using adb.
    """
    adb_command = ["C:\\Users\\aritt\\Desktop\\Android\\adb\\adb", "shell", "am", "start", "-a", "android.settings.SETTINGS"]
    subprocess.run(adb_command, check=True)

def navigate_to_element(element):
    """
    Navigate to the specified element.
    """
    if not d(text=element).exists(timeout=5):
        print(f"Cannot find '{element}'. Returning to settings.")
        start_settings_app()
        return False
    d(text=element).click()
    print(f"Clicked on '{element}'.")
    time.sleep(.1)  # Wait for the next screen to fully load
    return True

def navigate_and_act(actions):
    """
    Perform a series of navigation and actions.
    """
    for action in actions:
        elements = action.split(" > ")
        for i, element in enumerate(elements):
            if i == 0 and element.strip() == "Start Here":
                continue
            if not navigate_to_element(element):
                return

def main():
    if len(sys.argv) < 2:
        print("Usage: python find.py <sequence>")
        return
    sequence = sys.argv[1]
    actions = sequence.split(" > ")
    if not actions[0].strip() == "Start Here":
        start_settings_app()
    navigate_and_act(actions)

if __name__ == "__main__":
    main()
