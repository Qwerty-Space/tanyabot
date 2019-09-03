"""Dice roll

Will roll a __x__ sided dice __n__ times.  
Example:  `/roll 3d20`

pattern: `/roll (?:(\d+)d|d)?(\d+)$`
"""
from random import randint
from telethon import client, events
from .global_functions import log
import re


@events.register(events.NewMessage(pattern=r"(?<=\/roll ).*(?:(?<= )(?:(\d+)d|d)?(\d+)){1,10}"))
async def on_roll(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return

    m = event.pattern_match
    
    rollPattern = r"(?:(\d+)d|d)?(\d+){1,10}"
    
    matches = re.finditer(rollPattern, m)
    
    if not any(matches)
        await log(event, info="Bad format")
        return
    
    commands = list()
    outputs = list()
    total = int()
    
    for matchNum, match in enumerate(matches, start=1):
            
        if not match.group(2):
            rolls = 1
        else:
            rolls = int(match.group(1))

        sides = int(match.group(2))

        if rolls > 500 or sides > 100000:
            await event.respond("The maximum rolls is 500, and the maximum amount of sides is 100,000.")
            await log(event, info="Bad roll")
            return

        commands.append(f"{rolls}d{sides}")

        val = list()
        for _ in range(0, rolls):
            r = randint(1, sides)
            val.append(str(r))
            total += r

        ouputs.append(" ".join(val))
            
    command.join(commands)
    output = " ".join(outputs)

    await log(event)    # Logs the event
    await event.respond(f"**{command}:**\n`{output}`\n**=** `{total}`")
