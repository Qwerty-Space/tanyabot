r"""When a user mentions Hitler, or the Führer, the bot will respond with one of a few messages.

Limited to once a minute.

pattern:  `(?i)\b(hitler|f[uü]hrer)\b"` __(global)__
"""

import re
from random import randint
from telethon import events, sync
from .global_functions import log, cooldown


# MEIN FÜHRER!
@events.register(events.NewMessage(pattern=re.compile(r"(?i)\b(hitler|f[uü]hrer)\b").search, outgoing=False))
@cooldown(60)
async def mein_fuhrer(event):
    response_id = randint(0,3) # Roll for the response
    if response_id == 0:
        await event.reply("Heil Hitler!")
    elif response_id == 1:
        await event.reply("Sieg Heil!")
    elif response_id == 2:
        await event.reply(file="CAADAgADWgADraG3CP76-OQcP7msAg")
    elif response_id == 3:
        await event.reply(file="CAADBAADkQYAAhgwqgVYHov8PqiL9gI")
    await log(event, response_id)
