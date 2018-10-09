"""When a user mentions a person with "he", "she" or their
derivatives, the bot will respond with "Did you just assume their gender?!"

pattern:  `(?i)\b(he|his|she|her)\b`
"""

import re
from telethon import events, sync
from .global_functions import probability


# Did you just assume their gender?!
@events.register(events.NewMessage(pattern=re.compile(r"(?i)\b(he|his|she|her)\b").search, forwards=False))
async def assume(event):
    sender = await event.get_sender()
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    if probability(0.05):
        await event.reply("Did you just assume their gender?!")
