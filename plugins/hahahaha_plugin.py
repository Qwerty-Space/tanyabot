r"""When a user says "haha" (or any variant in length of), the bot
will respond with their message multiplied by a random number between 2 and 5.

Limits to once every 2 hours.

pattern:  `(?i)(hah?\w+a)$`
"""

import re
from random import randint
from datetime import datetime
from telethon import events, sync
from .global_functions import log, cooldown


# Hahahahahaha
@events.register(events.NewMessage(pattern=r"(?i)(hah?\w+a)$", outgoing=False))
@cooldown(7200)
async def haha(event):
    response_length = randint(2,5)
    response = event.pattern_match.group(1)*response_length    # Format the response (between 2 to 5 times the original length)
    await event.reply(response.capitalize())    # Capitalize the response
    await log(event, response_length)
