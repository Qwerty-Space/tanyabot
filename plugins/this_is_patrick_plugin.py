r"""Saying "is this __something__" will result in the bot replying with "No, this is Patrick."

pattern:  `(?i)^is this ((?:\S+ ?){1,4})\??$`
"""

import re
from telethon import events
from .global_functions import probability, log


# No, this is Patrick!
@events.register(events.NewMessage(pattern=r"(?i)^is this ((?:\S+ ?){1,4})\??$"))
async def this_is_patrick(event):
    outcome = probability(0.2)
    if outcome:
        await event.reply("No, this is Patrick.")
    await log(event, outcome)