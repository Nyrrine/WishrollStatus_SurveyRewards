#!/usr/bin/env python3

import pyautogui
import time
import sys
from colorama import init, Fore, Style
import json
import os
from datetime import datetime, timedelta

init(autoreset=True)

# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.5  # Pause between PyAutoGUI calls

class RetoolAutomation:
    def __init__(self):
        self.username_field_pos = None
        self.submit_button_pos = None
        self.processed_codes = set()
        self.successful_codes = []
        self.failed_codes = []
        self.start_time = None
        
    def setup_positions(self):
        """Let user click on the user code field and submit button positions"""
        print(f"\n{Fore.CYAN}=== SETUP MODE ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}We need to know where to click!{Style.RESET_ALL}\n")
        
        # User code field
        print(f"{Fore.GREEN}1. Move your mouse to the USER CODE INPUT FIELD{Style.RESET_ALL}")
        print(f"   Press {Fore.CYAN}Enter{Style.RESET_ALL} when your mouse is over it...")
        input()
        self.username_field_pos = pyautogui.position()
        print(f"   ✓ Captured position: {self.username_field_pos}")
        
        # Submit button
        print(f"\n{Fore.GREEN}2. Move your mouse to the SUBMIT/REWARD BUTTON{Style.RESET_ALL}")
        print(f"   Press {Fore.CYAN}Enter{Style.RESET_ALL} when your mouse is over it...")
        input()
        self.submit_button_pos = pyautogui.position()
        print(f"   ✓ Captured position: {self.submit_button_pos}")
        
        # Save positions
        self.save_positions()
        
        print(f"\n{Fore.GREEN}Setup complete!{Style.RESET_ALL}")
        
    def save_positions(self):
        """Save positions to file"""
        config = {
            'username_field': {'x': self.username_field_pos.x, 'y': self.username_field_pos.y},
            'submit_button': {'x': self.submit_button_pos.x, 'y': self.submit_button_pos.y}
        }
        with open('positions.json', 'w') as f:
            json.dump(config, f, indent=2)
            
    def load_positions(self):
        """Load positions from file"""
        if os.path.exists('positions.json'):
            with open('positions.json', 'r') as f:
                config = json.load(f)
                self.username_field_pos = pyautogui.Point(
                    config['username_field']['x'],
                    config['username_field']['y']
                )
                # Handle old config format
                if 'coffee_button' in config:
                    button_config = config['coffee_button']
                elif 'submit_button' in config:
                    button_config = config['submit_button']
                else:
                    return False
                
                self.submit_button_pos = pyautogui.Point(
                    button_config['x'],
                    button_config['y']
                )
                return True
        return False
    
    def clear_field(self):
        """Clear the user code field"""
        # Triple-click to select all
        pyautogui.click(self.username_field_pos, clicks=3)
        time.sleep(0.2)
        # Delete
        pyautogui.press('delete')
        
    def type_user_code(self, user_code):
        """Type user code in the field"""
        # Click on field
        pyautogui.click(self.username_field_pos)
        time.sleep(0.2)
        
        # Clear it first
        self.clear_field()
        time.sleep(0.2)
        
        # Type user code
        pyautogui.typewrite(user_code, interval=0.05)
        
    def click_submit_button(self):
        """Click the submit button"""
        pyautogui.click(self.submit_button_pos)
        
    def display_progress(self, current_code, current_index, total_codes):
        """Display progress"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Progress
        progress = (current_index / total_codes) * 100
        bar_length = 40
        filled = int(bar_length * current_index // total_codes)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"\n{Fore.CYAN}🎁 RETOOL AUTOMATION 🎁{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        print(f"Progress: [{Fore.GREEN}{bar}{Style.RESET_ALL}] {progress:.1f}%")
        print(f"Codes: {current_index}/{total_codes}")
        
        # Stats
        print(f"\n{Fore.GREEN}✓ Successful: {len(self.successful_codes)}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Failed: {len(self.failed_codes)}{Style.RESET_ALL}")
        
        # Time
        if self.start_time:
            elapsed = time.time() - self.start_time
            if current_index > 0:
                avg_time = elapsed / current_index
                remaining = (total_codes - current_index) * avg_time
                eta = str(timedelta(seconds=int(remaining)))
                print(f"\nETA: {eta}")
        
        print(f"\n{Fore.YELLOW}Processing: {current_code}{Style.RESET_ALL}")
        print(f"\n{Style.DIM}Move mouse to top-left corner to abort{Style.RESET_ALL}")
        
    def process_codes(self, codes_file):
        """Process all user codes"""
        # Load user codes
        with open(codes_file, 'r') as f:
            codes = [line.strip() for line in f if line.strip()]
        
        print(f"\n{Fore.CYAN}Loaded {len(codes)} user codes{Style.RESET_ALL}")
        
        # Countdown
        print(f"\n{Fore.YELLOW}Starting in 10 seconds...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Switch to your browser window!{Style.RESET_ALL}")
        for i in range(10, 0, -1):
            print(f"{Fore.GREEN}{i}...{Style.RESET_ALL}")
            time.sleep(1)
        
        self.start_time = time.time()
        
        # Process each code
        for i, code in enumerate(codes):
            if code in self.processed_codes:
                continue
                
            try:
                self.display_progress(code, i, len(codes))
                
                # Type user code
                self.type_user_code(code)
                time.sleep(2)  # Wait for button to enable
                
                # Click submit button
                self.click_submit_button()
                
                # Wait for processing
                print(f"\n{Fore.CYAN}Waiting for reward to process...{Style.RESET_ALL}")
                time.sleep(2)
                
                self.successful_codes.append(code)
                self.processed_codes.add(code)
                
            except pyautogui.FailSafeException:
                print(f"\n{Fore.RED}Aborted by user!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error processing {code}: {e}{Style.RESET_ALL}")
                self.failed_codes.append(code)
                self.processed_codes.add(code)
                
            # Save progress periodically
            if (i + 1) % 10 == 0:
                self.save_progress()
        
        # Final save
        self.save_progress()
        self.show_summary()
        
    def save_progress(self):
        """Save progress to files"""
        # Save successful codes
        with open('successful_users.txt', 'w') as f:
            for code in self.successful_codes:
                f.write(f"{code}\n")
        
        # Save failed codes
        with open('failed_users.txt', 'w') as f:
            for code in self.failed_codes:
                f.write(f"{code}\n")
                
        # Save state
        state = {
            'processed': list(self.processed_codes),
            'successful': self.successful_codes,
            'failed': self.failed_codes,
            'last_run': datetime.now().isoformat()
        }
        with open('progress.json', 'w') as f:
            json.dump(state, f, indent=2)
            
    def show_summary(self):
        """Show final summary"""
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ COMPLETE!{Style.RESET_ALL}")
        print(f"\nTotal processed: {len(self.processed_codes)}")
        print(f"{Fore.GREEN}Successful: {len(self.successful_codes)}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {len(self.failed_codes)}{Style.RESET_ALL}")
        
        if self.failed_codes:
            print(f"\n{Fore.YELLOW}Failed codes saved to failed_users.txt{Style.RESET_ALL}")

def main():
    automation = RetoolAutomation()
    
    # Check if we need setup
    if not automation.load_positions() or '--setup' in sys.argv:
        automation.setup_positions()
    else:
        print(f"{Fore.GREEN}Using saved positions{Style.RESET_ALL}")
    
    # Get filename
    if len(sys.argv) > 1 and sys.argv[1] != '--setup':
        usernames_file = sys.argv[1]
    else:
        usernames_file = 'usernames.txt'
    
    # Check file exists
    if not os.path.exists(usernames_file):
        print(f"{Fore.RED}File not found: {usernames_file}{Style.RESET_ALL}")
        return
    
    # Process codes
    automation.process_codes(usernames_file)

if __name__ == "__main__":
    main()