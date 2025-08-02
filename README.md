# Retool Survey Reward System Automation Tool 🎁

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Retool](https://img.shields.io/badge/Retool-3D3D3D?style=for-the-badge&logo=retool&logoColor=white)

A Windows automation tool for bulk user code input in Retool to distribute survey rewards using PyAutoGUI for mouse and keyboard automation.

## Features

- Click-based automation with position setup
- Bulk processing of multiple user codes
- Progress tracking with colored output
- Smart rate limiting (4-second minimum between inputs)
- Automatic position saving and loading
- Results saved to separate files

## Prerequisites

- Windows 10 or 11
- Python 3.x installed ([Download from python.org](https://www.python.org/downloads/))
- Web browser with Retool application

## Installation (Windows)

1. **Download the code:**
   - Click the green "Code" button on GitHub
   - Select "Download ZIP"
   - Extract the ZIP file to a folder on your computer (e.g., `C:\Users\YourName\Desktop\retool-automation`)

2. **Open Command Prompt:**
   - Press `Windows + R`
   - Type `cmd` and press Enter
   - Navigate to the folder where you extracted the files. For example:
     ```cmd
     cd C:\Users\YourUsername\Desktop\retool-automation
     ```
     (Replace "YourUsername" with your actual Windows username and adjust the path to where you extracted the files)

3. **Install required dependencies:**
   ```cmd
   pip install pyautogui colorama
   ```
   
   If you get an error, try:
   ```cmd
   python -m pip install pyautogui colorama
   ```

4. **Run the setup immediately after installation:**
   ```cmd
   python retool_automation.py --setup
   ```
   This will configure the tool for your screen - you MUST do this before first use!

## Setup

1. Create a `usernames.txt` file in the project directory
2. Add one user code per line:
```
ABC123
DEF456
GHI789
```

3. Make sure you're logged into your Retool application

## Usage

### First Time Setup (Required!)

1. **Prepare your browser:**
   - Open Retool in your browser
   - Navigate to the survey reward distribution page
   - Make sure the input field and submit button are visible on screen

2. **Run the setup command:**
   
   **Option A - Using Command Prompt:**
   Here's exactly what to type in Command Prompt:
   ```cmd
   C:\Users\YourUsername\Desktop\retool-automation>python retool_automation.py --setup
   ```
   
   What you'll see:
   ```
   === SETUP MODE ===
   We need to know where to click!
   
   1. Move your mouse to the USER CODE INPUT FIELD
      Press Enter when your mouse is over it...
   ```
   
   **Option B - Using the batch file (easier):**
   - Double-click `run.bat` in the folder
   - It will install dependencies and run the script automatically

3. **Follow the setup prompts:**
   - When you see "Move your mouse to the USER CODE INPUT FIELD":
     - Move your mouse cursor over the input field where you type user codes
     - Press Enter on your keyboard
   - When you see "Move your mouse to the SUBMIT/REWARD BUTTON":
     - Move your mouse cursor over the submit/reward button
     - Press Enter on your keyboard
   - You'll see "Setup complete!" when done

4. **The setup is saved!** You only need to do this once unless the page layout changes.

### Running the Automation

1. Make sure Retool is open and you're on the reward page

2. Run the script:

   **Option A - Command Prompt:**
   Full example of what to type:
   ```cmd
   C:\Users\YourUsername\Desktop\retool-automation>python retool_automation.py
   ```
   
   What you'll see:
   ```
   Using saved positions
   
   Loaded 25 user codes
   
   Starting in 10 seconds...
   Switch to your browser window!
   10...
   9...
   8...
   ```
   
   **Option B - Double-click run.bat (easier):**
   - Just double-click the `run.bat` file
   - It will automatically start the script

3. You have 10 seconds to switch to your browser window before it starts

The tool will:
- Clear and type each user code from `usernames.txt`
- Click the submit button for each code
- Wait 4 seconds between submissions (rate limiting)
- Save successful submissions to `successful_users.txt`
- Save failed attempts to `failed_users.txt`

## Output Files

- `successful_users.txt` - List of user codes that were successfully processed
- `failed_users.txt` - List of user codes where the submission failed

## Safety Features

- **Failsafe**: Move mouse to top-left corner to abort script
- **Rate limiting**: 4-second minimum wait between sends
- **Position memory**: Saves click positions in `positions.json`
- All user data files are excluded from version control (.gitignore)

## Troubleshooting

If you encounter issues:
- Make sure the browser window is visible and not minimized
- Check that usernames in `usernames.txt` are valid
- If clicks are missing, delete `positions.json` and re-run setup with `python retool_automation.py --setup`
- Move mouse to top-left corner to emergency stop the script

### Re-running Setup
If the button or input field location changes, or clicks aren't working:
```cmd
python retool_automation.py --setup
```
Or just run `run.bat` and add `--setup` when prompted.

## Important Windows Notes

- **This tool uses mouse automation** - it will control your mouse and keyboard
- **This only works for windows** - PyAutoGUI requires native Windows
- Keep the browser window visible and in focus during automation
- Disable any screen savers or auto-lock features while running