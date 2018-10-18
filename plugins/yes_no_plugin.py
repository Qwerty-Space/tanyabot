r"""Adding "yes or no" to the end of your message will result in a yes or no answer from the bot.
Also supports "y/n", and other alternatives.

pattern:  `(?i)(yes|y)(/| or )(no|n)\??$`
"""

import re
from telethon import events
from .global_functions import probability, log


# Yes or no
# Matches "y/n" "yes or no" "yes/no?" etc
@events.register(events.NewMessage(pattern=re.compile(r"(?i)(yes|y)(/| or )(no|n)\??$").search, forwards=False))
async def yes_or_no(event):
    outcome = probability(0.5)
    await log(event, outcome)
    if outcome:
        await event.reply("Yes.")
    else:
        await event.reply("No.")
