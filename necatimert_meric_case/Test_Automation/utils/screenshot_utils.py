import os

def take_screenshot(driver, file_name):
    """Capture a screenshot of the current browser window."""
    try:
        # Ensure file_name has the .png extension if not provided
        if not file_name.endswith(".png"):
            file_name += ".png"

        # Get the absolute path of the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Define the path to the output/screenshots folder
        screenshot_path = os.path.join(project_dir, "output", "screenshots")

        # Create the folder if it doesn't exist
        os.makedirs(screenshot_path, exist_ok=True)

        # Define the full path for the screenshot file
        file_path = os.path.join(screenshot_path, file_name)

        # Save the screenshot
        driver.save_screenshot(file_path)
        print(f"Screenshot saved to {file_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
