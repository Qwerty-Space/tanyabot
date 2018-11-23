r"""Saying "is this __something__" will result in the bot replying with "No, this is Patrick."

Limits to once a minute.

pattern:  `(?i)^is this ((?:\S+ ?){1,3})\??$`
"""

import re
from telethon import events
from .global_functions import log, cooldown


# No, this is Patrick!
@events.register(events.NewMessage(pattern=r"(?i)^is this ((?:\S+ ?){1,3})\??$"))
@cooldown(60)
async def this_is_patrick(event):
    await event.reply("No, this is Patrick.")
    await log(event)