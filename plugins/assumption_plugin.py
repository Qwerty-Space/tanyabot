"""When a user mentions a person with "he", "she" or their
derivatives, the bot will respond with "Did you just assume their gender?!"

pattern:  `(?i)\b(he|his|she|her)\b`(global)
"""

import re
from telethon import events, sync
from .global_functions import probability, log


# Did you just assume their gender?!
@events.register(events.NewMessage(pattern=re.compile(r"(?i)\b(he|his|she|her)\b").search, forwards=False))
async def assume(event):
    outcome = probability(0.05)
    if outcome:
        await event.reply("Did you just assume their gender?!")
    await log(event, outcome)
