"""If you say "love you botname/username" the bot will respond with "love you too!"
It also works with other words, like "fuck", "screw", "damn"

pattern:  `(?i)(love|fuck|screw|damn?) (yo)?u @?({fname}|{name}|{username})`
"""

import re
from telethon import events, sync
from .global_functions import log


# Insult
@events.register(events.NewMessage(pattern=r"(?i)(love|fuck|screw|damn?) (yo)?u @?(.+)", outgoing=False, forwards=False))
async def insult(event):
    name = (await event.client.get_me()).first_name
    fname = re.sub(r"\W.+", "", name)
    username = (await event.client.get_me()).username
    if re.match(fr"(?i)({fname}|{name}|{username})", event.pattern_match.group(3)):
        await log(event)
        await event.reply(event.pattern_match.group(1)+" you too!")    # "Love you too!"
