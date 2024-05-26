import uiautomator2 as u2
import subprocess
import sys

def start_settings_app(device):
    adb_command = ["adb", "-s", device, "shell", "am", "start", "-a", "android.settings.SETTINGS"]
    result = subprocess.run(adb_command, capture_output=True, text=True)
    if "Warning: Activity not started" in result.stderr:
        print("Settings app already active.")
    else:
        print("Launched Settings app.")

def navigate_to_element(d, device, element, next_element=None, missed_elements=None):
    if element.strip() == "Start Here":
        print("Acknowledged 'Start Here' as a directive, not a UI element. Continuing.")
        return True

    try:
        if not d(text=element).exists(timeout=10):
            if not scroll_to_element(d, element):
                raise u2.UiObjectNotFoundError
        d(text=element).click()
        print(f"Clicked on '{element}'.")
        if next_element and not d(text=next_element).exists(timeout=10):
            print(f"Failed to navigate to the next screen after clicking '{element}'.")
            if missed_elements is not None:
                missed_elements.append(next_element)
            return False
    except u2.UiObjectNotFoundError:
        print(f"Cannot find '{element}' after extensive searching. Returning to settings.")
        if missed_elements is not None:
            missed_elements.append(element)
        start_settings_app(device)
        return False
    return True

def scroll_to_element(d, element):
    """
    Modified to scroll through the screen more slowly, checking for the element's presence 
    after each small scroll, instead of flinging to the ends.
    """
    for _ in range(10):  # Try scrolling up to 10 times.
        if d(scrollable=True).scroll.vert.forward(steps=100):
            if d(text=element).exists:
                return True
        else:
            break  # Break if we can't scroll further.

    # If not found, scroll back to the beginning and try once more.
    d(scrollable=True).scroll.toBeginning()
    for _ in range(10):  # Try scrolling again up to 10 times.
        if d(scrollable=True).scroll.vert.forward(steps=100):
            if d(text=element).exists:
                return True
        else:
            break  # Break if we can't scroll further.

    return False

def navigate_and_act(device, actions):
    d = u2.connect(device)
    missed_elements = []
    for action in actions:
        elements = action.split(" > ")
        for i, element in enumerate(elements):
            next_element = elements[i + 1] if i + 1 < len(elements) else None
            if not navigate_to_element(d, device, element, next_element, missed_elements):
                continue  # Log but continue to try next actions

    if missed_elements:
        print("Summary of missed elements:")
        for missed in missed_elements:
            print(f"- {missed}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <device_serial> <sequence>")
        sys.exit(1)
    device_serial = sys.argv[1]
    sequence = sys.argv[2]
    actions = sequence.split(" > ")

    navigate_and_act(device_serial, actions)

if __name__ == "__main__":
    main()
