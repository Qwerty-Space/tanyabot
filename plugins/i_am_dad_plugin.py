r"""When a user says "I'm __something__", (up to three words) the bot will respond with "Hi something"

Limts to once every 2 hours.

pattern:  `(?i)^(?:i'?m|i am) ((?:\S+ ?){1,3})$`
"""

from telethon import events, sync
from .global_functions import log, cooldown

# Hi, Hungry!
# Check if they say "I am" "I'm" or any variant of (+ at least 1, but at most 3 words)
@events.register(events.NewMessage(pattern=r"(?i)^(?:i'?m|i am) ((?:\S+ ?){1,3})$", outgoing=False, forwards=False))
@cooldown(7200)
async def i_am_dad(event):
    await event.reply("Hi " + event.pattern_match.group(1)) 
    await log(event)
