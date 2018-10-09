"""If you say "love you botname/username" the bot will respond with "love you too!"
It also works with other words, like "fuck", "screw", "damn"

pattern:  `(?i)(love|fuck|screw|damn?) (yo)?u @?({fname}|{name}|{username})`
"""

import re
from telethon import events, sync
from .global_functions import probability


# Insult
@events.register(events.NewMessage(pattern=r"(?i)(love|fuck|screw|damn?) (yo)?u @?(.+)", outgoing=False, forwards=False))
async def insult(event):
    name = (await event.client.get_me()).first_name
    fname = re.sub(r"\W.+", "", name)
    username = (await event.client.get_me()).username
    if re.match(fr"(?i)({fname}|{name}|{username})", event.pattern_match.group(3)):
        sender = await event.get_sender()
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        await event.reply(event.pattern_match.group(1)+" you too!")    # "Love you too!"
