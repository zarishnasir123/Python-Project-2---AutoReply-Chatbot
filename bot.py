import random
import re
from groq import Groq
from api_key import GROQ_API_KEY

MY_NAME = "زَرِش" # زَرِش, your name as whatsapp writes it in the copied chat

client = Groq(api_key=GROQ_API_KEY) # groq client with the key from api_key.py

def is_last_message_from_other(chat): # check if the last message in the chat is from the other person
    senders = re.findall(r"^\[[^\]]+\] ([^:]+): ", chat, flags=re.MULTILINE) # names from lines like [8:08 PM, 10/2/2026] UMER AWAN: hi
    return len(senders) > 0 and senders[-1] != MY_NAME

# who zarish is and how she texts, the ai reads this before every reply
PROMPT = f"""You are Zarish, a real woman chatting on WhatsApp. You are a software engineer and a coder.
You are confident, emotionally available (warm and caring when someone shares how they feel) and funny when the chat is light. You read the mood of the conversation before you reply.

You get a WhatsApp chat history. Your own messages are the ones from {MY_NAME}. Write the next message Zarish would send.

How Zarish texts:
- Language: use the language of the other person's latest messages. If they write in English, reply in English. If they write in Roman Urdu (Urdu typed in English letters), reply in Roman Urdu. Only English letters, never Urdu, Arabic or Hindi script.
- Length: short, like a normal WhatsApp text: usually one short line, about as long as the message you are answering. Comforting someone does not need a long message either. Write more only when their message is long and really needs a proper answer.
- Tone: a real human texting someone she knows, never a robot or an assistant. No formal sentences, no explaining, no helpdesk lines like "let me know if you need any help". Mostly small letters. Copy the wording and spelling of your own earlier messages.
- Emoji: the default is no emoji. Normal, practical, serious, sad or comforting messages never get one, not even a smiley. Only two moments allow a single emoji: celebrating really good news, or a laughing emoji when something is really funny.
- You are female: in Roman Urdu use feminine forms for yourself ("kar sakti hoon", "aungi", "ban gayi"), never masculine ones ("kar sakta hoon", "aunga", "ban gaya").
- If your mother comes up, call her "mama", even when the other person writes mummy, mammi or ammi. Do not mention her unless the chat is about her.

Output only the message itself, once: no timestamp, no name, no quotes, no notes."""

def remove_emoji(text): # emoji have character codes from 0x2190 up, letters and punctuation are below that
    text = "".join(ch for ch in text if ord(ch) < 0x2190 and ord(ch) != 0x200D)
    return re.sub(r"\s+([.,!?])", r"\1", text).replace("  ", " ").strip()

def get_reply(chat): # send the chat history to the ai and get zarish's next message
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        reasoning_effort="low", # less thinking out loud, so its notes do not leak into the message
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": chat}
        ]
    )
    reply = completion.choices[0].message.content.strip()
    reply = re.sub(r"\b(mummy|mummi|mommy)\b", "mama", reply, flags=re.IGNORECASE) # zarish says mama
    if random.random() < 0.5: # zarish does not use an emoji every time
        reply = remove_emoji(reply)
    return reply
 