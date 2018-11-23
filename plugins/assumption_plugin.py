r"""When a user mentions a person with "he", "she" or their
derivatives, the bot will respond with "Did you just assume their gender?!"

Has a 50% chance of happening every 12 hours.

pattern:  `(?i)\b(he|his|she|her)\b`(global)
"""

import re
from telethon import events, sync
from .global_functions import probability, log, cooldown


# Did you just assume their gender?!
@events.register(events.NewMessage(pattern=re.compile(r"(?i)\b(he|his|she|her)\b").search, forwards=False))
@cooldown(43200)
async def assume(event):
    outcome = probability(0.5)
    if outcome:
        await event.reply("Did you just assume their gender?!")
    await log(event, outcome)
