r"""
When a user says "haha" (or any variant in length of), the bot
will respond with their message multiplied by a random number between 2 and 5.

pattern:  `(?i)(hah?\w+a)$`
"""

import re
from random import randint
from datetime import datetime
from telethon import events, sync
from .global_functions import probability


# Hahahahahaha
@events.register(events.NewMessage(pattern=re.compile(r"(hah?\w+a)$", re.I).match, outgoing=False))
async def haha(event):
    sender = await event.get_sender()
    response_length = randint(2,5)
    response = event.pattern_match.group(1)*response_length    # Format the response (between 2 to 5 times the original length)
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}: {response_length}")
    if probability(0.2):
        await event.reply(response.capitalize())    # Capitalize the response
