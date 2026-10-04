# WhatsApp AutoReply Chatbot

A Python bot that answers WhatsApp messages for you. It watches the chat that is open in WhatsApp Web, and when the other person writes, it asks an AI model to write a reply in your own texting style and sends it.

It works by moving the mouse and pressing keys on your own screen with PyAutoGUI. It does not use any WhatsApp API.

> **Read this before you run it**
>
> - The bot sends real messages in your name without asking you first. The AI can misread a message or make things up.
> - WhatsApp's Terms of Service do not allow automated messaging, and accounts can be banned for it. This is a learning project. Use it at your own risk.
> - The text of the open chat is sent to Groq so the AI can write a reply.

## How it works

1. It finds the Chrome window that shows WhatsApp Web and brings it to the front.
2. It scrolls the open chat down to the newest message.
3. It selects the visible chat by dragging the mouse from the first message bubble to the bottom-right corner, then copies it.
4. It reads the copied text. WhatsApp copies every message as `[time, date] name: message`, so the bot can tell who wrote the last one.
5. If the last message is from the other person, it sends the chat text to an AI model on Groq, together with a description of how you text. It pastes the reply into the message box and presses Enter.
6. It waits 10 seconds and starts again.

## Files

| File | What it does |
|---|---|
| `main.py` | The bot itself: copies the chat, decides whether to reply, sends the reply, and repeats. |
| `bot.py` | The AI part: the description of your personality (`PROMPT`), the call to Groq, and the check for who sent the last message. |
| `get_cursor.py` | A helper that prints the mouse position, for measuring screen positions. |
| `api_key.py` | Your Groq API key. It is not in this repository; you create it yourself in Setup. |

## Requirements

- Windows (built and tested on Windows 11)
- Python 3 (tested with 3.13)
- Google Chrome with WhatsApp Web logged in and set to the **dark theme**
- A 1920×1080 screen with Chrome maximised (tested at 125% display scaling)
- A Groq API key (Groq had a free tier with no card needed when this was written)

Tested with pyautogui 0.9.54, pyperclip 1.11.0, groq 1.7.0 and Pillow 12.0.0.

## Setup

1. Download the project and install the packages:

   ```
   git clone https://github.com/zarishnasir123/Python-Project-2---AutoReply-Chatbot.git
   cd Python-Project-2---AutoReply-Chatbot
   pip install pyautogui pyperclip groq pillow
   ```

2. Create a key at <https://console.groq.com/keys>. Then make a file named `api_key.py` next to `main.py` with this one line:

   ```python
   GROQ_API_KEY = "paste-your-key-here"
   ```

   `api_key.py` is listed in `.gitignore`, so git will not upload it. Never share the key or paste it anywhere else.

3. In `bot.py`, set `MY_NAME` to your own name exactly as WhatsApp writes it in a copied chat. To find it, select a few messages in WhatsApp Web, copy them and paste them into Notepad. Your own messages look like `[8:08 PM, 10/2/2026] Your Name: hi`. The bot uses this name to tell your messages from the other person's.

4. In `bot.py`, rewrite `PROMPT` so it describes you. It currently describes the author.

5. If your screen is not 1920×1080, measure the positions again. Run `python get_cursor.py`, hover the mouse over each spot below, note the numbers it prints, and press Ctrl+C to stop. Then change the numbers in `main.py`.

   | Position in `main.py` | Where it is on the screen |
   |---|---|
   | `740, 200` | Top-left corner of the chat, just below the contact name |
   | `1890, 930` | Bottom-right corner of the chat, just above the message box |
   | `1200, 973` | The message box |
   | `740` and `1830` in `find_first_message_y` | The left edge of the other person's bubbles and the right edge of your own |

## Usage

1. Open WhatsApp Web in Chrome and open the chat you want the bot to answer. WhatsApp must be the tab you can see.
2. Run the bot:

   ```
   python main.py
   ```

3. Leave the mouse and keyboard alone while it runs. The terminal prints every reply it sends.

To stop the bot, push the mouse into the top-left corner of the screen, or click on any other window.

## Changing how it replies

The personality lives in `PROMPT` in `bot.py`. It sets the language (English or Roman Urdu, whichever the chat is using), the tone, when an emoji is allowed, and which words to use. Edit that text to change how the bot talks.

The model is set in `get_reply` in `bot.py` (`openai/gpt-oss-120b`). Groq changes its list of models over time. If the bot prints a model error, choose a current model in the Groq console and put its name there.

## Limitations

- **One chat only.** It replies in the chat that is open, not in all your chats.
- **Your computer is busy while it runs.** The PC must stay on with WhatsApp Web visible, and the bot moves the mouse every 10 seconds.
- **It only reads what is on the screen.** Older messages that are scrolled out of view are not sent to the AI.
- **Text only.** Photos, voice notes and stickers are not read.
- **Fixed positions and colours.** It breaks if the window size, the browser zoom or the WhatsApp theme changes. The colours in `main.py` are the bubble colours of the dark theme.
- **The first message on screen may be skipped** when it is half hidden under the contact name or starts with a quoted reply.
- **Free limits.** Groq limits how many requests a free key can make. When the limit is reached, the bot prints the error and tries again on the next round.
