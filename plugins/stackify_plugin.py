r"""Converts an amount of blocks to an amount of Minecraft stacks.
Examples:
• 635 blocks
• 635 blocks in/as stacks
• 635 in/as stacks

Add `s16` to the end to change the maximum stack size to 16 for items such as snowballs.

pattern:  `(?i)(\d+){1,9}(?: blocks)?(?: (?:in|as) stacks)?(?: s(16|64))?`
"""

from telethon import events, sync
from .global_functions import log, cooldown

def plural(number):
    if number == 1:
        return ""
    else:
        return "s"

# Calculate how many stacks
@events.register(events.NewMessage(pattern=r"(?i)(\d+){1,9}(?: blocks)?(?: (?:in|as) stacks)?(?: s(16|64))?", forwards=False))
async def stackify(event):
    """First calcuate how many full stacks, then the remainder."""

    m = event.pattern_match

    blocks = int(m.group(1))
    one_stack = int(m.group(2)) if m.group(2) else 64

    stacks = int(blocks / one_stack)
    remainder = blocks % one_stack

    await log(event, f"{one_stack}, {stacks} + {remainder}")
    total = f"**{blocks} block{plural(blocks)} is:**\n`{stacks} stack{plural(stacks)} and {remainder} block{plural(remainder)}`"

    await event.reply(total)
