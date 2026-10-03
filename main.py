import pyautogui
import pyperclip
import time
from bot import get_reply, is_last_message_from_other

# chrome tab position: 1268, 1041
# chat top-left corner (drag start): 740, 200
# chat bottom-right corner: 1890, 930
# message box: 1200, 973

GREY = (36, 38, 38) # bubble colour of the other person's messages (whatsapp dark theme)
GREEN = (20, 77, 55) # bubble colour of my messages (whatsapp dark theme)

def find_first_message_y(): # the drag only selects when it starts on a message, so find the first whole bubble below the name
    screen = pyautogui.screenshot()
    for y in range(195, 880):
        for x, colour in [(740, GREY), (1830, GREEN)]: # left edge of their bubbles, right edge of mine
            if screen.getpixel((x, y - 1)) != colour and screen.getpixel((x, y)) == colour and screen.getpixel((x, y + 15)) == colour:
                return y + 18 # the first line of text in that bubble
    return 200 # no bubble found, use the corner

pyautogui.click(1268, 1041) # click the chrome icon to open whatsapp
pyautogui.moveTo(740, 200) # go to the top-left corner of the chat, just below the name
time.sleep(2) # wait for the window to come to the front

if "WhatsApp" not in (pyautogui.getActiveWindowTitle() or ""): # don't drag on the wrong window
    raise SystemExit("WhatsApp is not in front, stopping.")

pyautogui.scroll(-5000) # scroll down to the newest message
pyautogui.moveTo(740, 150) # rest on the name so no message is highlighted by the mouse
time.sleep(1) # wait for the scrolling to stop

pyperclip.copy("") # empty the clipboard so an old copy is not mistaken for the chat
pyautogui.moveTo(740, find_first_message_y()) # top-left corner of the chat, on the first message
pyautogui.mouseDown(button='left') # hold the left button
time.sleep(0.3)
pyautogui.moveTo(1890, 930, duration=1.5) # drag to the bottom-right corner to select the chat
time.sleep(0.3)
pyautogui.mouseUp(button='left') # release the button

pyautogui.hotkey('ctrl', 'c') # copy the selected chat to the clipboard
time.sleep(0.5) # wait for the clipboard to update
pyautogui.click(1200, 973) # click the message box to remove the selection

chat = pyperclip.paste() # take the copied chat in a variable
print(chat)

if chat == "":
    print("Nothing was copied from the chat, not replying.")
elif is_last_message_from_other(chat): # only reply when the other person sent the last message
    reply = get_reply(chat) # ask the ai for zarish's reply
    print(reply)

    pyperclip.copy(reply) # copy the reply to the clipboard
    pyautogui.click(1200, 973) # click the message box
    pyautogui.hotkey('ctrl', 'v') # paste the reply
    time.sleep(1) # wait for the paste to land in the message box
    pyautogui.press('enter') # send the reply
else:
    print("The last message is yours, not replying.")
