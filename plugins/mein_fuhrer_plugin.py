r"""When a user mentions Hitler, or the Führer, the bot will respond with one of a few messages.

Limited to once a minute.

pattern:  `(?i)\b(hitler|f[uü]hrer)\b"` __(global)__
"""

import re
from random import randint, choice
from telethon import events, sync
from .global_functions import log, cooldown

response_list = ["CAADAgADWgADraG3CP76-OQcP7msAg", # Tanya
                 "CAADBAADkQYAAhgwqgVYHov8PqiL9gI", # The Professor
                 "CAADAgADRQADqh-tD2oBxZyI7uVhAg" # Azunyan
                ]

# MEIN FÜHRER!
@events.register(events.NewMessage(
            pattern=re.compile(r"(?i)\b(hitler|f[uü]hrer|(14)?88|HH)\b").search,
            outgoing=False))
@cooldown(60)
async def mein_fuhrer(event):
    response_id = choice(response_list) # Roll for the response

    await event.reply(file=response_id)

    await log(event, response_list.index(response_id))
