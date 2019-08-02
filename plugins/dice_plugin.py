"""Start message

pattern: `/start$`
"""
from random import randint
from telethon import client, events
from .global_functions import log


# /start
# @events.register(events.NewMessage(pattern=r"/roll(@\w+)? (\d+)$"))
@events.register(events.NewMessage(pattern=r"/roll(@\w+)? (?:(\d+)d|d)?(\d+)$"))
async def on_roll(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return

    m = event.pattern_match

    if not m.group(2):
        rolls = 1
    else:
        rolls = int(m.group(2))

    sides = int(m.group(3))

    if rolls > 500 or sides > 100000:
        await event.respond("The maximum rolls is 500, and the maximum amount of sides is 100,000.")
        await log(event, info="Bad roll")
        return

    command = f"{rolls}d{sides}"

    val = list()
    total = int()
    for _ in range(0, rolls):
        r = randint(1, sides)
        val.append(str(r))
        total += r

    output = " ".join(val)

    await log(event)    # Logs the event
    await event.respond(f"**{command}:**\n`{output}`\n**=**`{total}`")
