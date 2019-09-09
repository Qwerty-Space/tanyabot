"""Dice roll
Will roll a __x__ sided dice __n__ times.  
Example:  `/roll 3d20`

pattern: `/roll (?:(\d+)d|d)?(\d+)$`
"""
from random import randint
from telethon import client, events
from .global_functions import log
import re


@events.register(events.NewMessage(pattern=r"\/roll(?:@\w+)?.*(?:(\d+)d|d)(\d+)"))
async def on_roll(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return

    m = event.pattern_match[0]
    
    rollPattern = r"(?:\s(?:(\d+)d|d)(\d+))"
    
    matches = re.finditer(rollPattern, m)
    
    commands = list()
    outputs = list()
    total = int()
    outputStrings = list()
    
    for matchNum, match in enumerate(matches, start=1):
        
        if match.group(1) is None:
            rolls = 1
        else:
            rolls = int(match.group(1))

        sides = int(match.group(2))
        if rolls > 50 or sides > 100000:
            await event.respond("The maximum rolls is 50, and the maximum amount of sides is 100,000.")
            await log(event, info="Bad roll")
            return

        if sides < 1:
            await log(event, "No Dice Rolled")
            return

        commands.append(f"{rolls}d{sides}")
        outputStrings.append(f"**{rolls}d{sides}:**\n")

        val = list()
        for _ in range(0, rolls):
            r = randint(1, sides)
            val.append(str(r))
            total += r

        outputs.append(" ".join(val))
        outputStrings.append("`" + " ".join(val) + "`\n")
            
    command = " ".join(commands)
    output = "\n".join(outputs)

    
    if total == 0:
        await log(event, info="No Dice Rolled")
        return

    outputString = "".join(outputStrings)

    await log(event)    # Logs the event
#    await event.respond(f"**{command}:**\n`{output}`\n**=** `{total}`")
    await event.respond(f"{outputString}**=** `{total}`")
