r"""Saying "is this something" will result in the bot replying with "No, this is Patrick."

pattern:  `^is this ((?:\S+ ?){1,4})\??$`
"""

import re
from telethon import events, sync
from .global_functions import probability


# No, this is Patrick!
@events.register(events.NewMessage(pattern=re.compile(r"^is this ((?:\S+ ?){1,4})\??$", re.I).search))
async def this_is_patrick(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.2):
        await event.reply("No, this is Patrick.")
