import pyautogui

try:
    while True:
        a = pyautogui.position() # get the current mouse position
        print(a)
except KeyboardInterrupt: # Ctrl+C stops the loop
    print("Stopped.")
