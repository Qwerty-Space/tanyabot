r"""
When a user mentions Hitler, or the Führer, the bot will respond with one of three messages.

pattern:  `(?i)\b(hitler|führer|fuhrer)\b`
"""

import re
from random import randint
from telethon import events, sync
from .global_functions import probability, log


# MEIN FÜHRER!
@events.register(events.NewMessage(pattern=r"(?i)\b(hitler|führer|fuhrer)\b", outgoing=False))
async def mein_fuhrer(event):
    outcome = probability(0.4)
    response_id = randint(0,3) # Roll for the response
    if outcome:
        if response_id == 0:
            await event.reply("Heil Hitler!")
        elif response_id == 1:
            await event.reply("Sieg Heil!")
        elif response_id == 2:
            await event.reply(file="CAADAgADWgADraG3CP76-OQcP7msAg")
        elif response_id == 3:
            await event.reply(file="CAADBAADkQYAAhgwqgVYHov8PqiL9gI")
    await log(event, f"{outcome}, {response_id}")
