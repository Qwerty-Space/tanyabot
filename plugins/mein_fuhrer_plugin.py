r"""When a user mentions Hitler, or the Führer, the bot will respond with one of a few messages.

Limited to once a minute.

pattern:  `(?i)\b(hitler|f[uü]hrer)\b"` __(global)__
"""

import re
from random import randint, choice
from telethon import events, sync
from .global_functions import log, cooldown


# MEIN FÜHRER!
@events.register(events.NewMessage(pattern=re.compile(r"(?i)\b(hitler|f[uü]hrer)\b").search, outgoing=False))
@cooldown(60)
async def mein_fuhrer(event):
    response_list = ["CAADAgADWgADraG3CP76-OQcP7msAg", "CAADBAADkQYAAhgwqgVYHov8PqiL9gI", "CAADAgADRQADqh-tD2oBxZyI7uVhAg"]
    response_id = choice(response_list) # Roll for the response

    await event.reply(file=response_id)

    await log(event, response_list.index(response_id))
