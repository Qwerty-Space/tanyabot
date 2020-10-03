"""Whitelist

Only stay in groups in the whitelist
"""


from asyncio import sleep
from telethon import client, events, errors
from .global_functions import log, cooldown


whitelist = {
    1142596298, # Logs
    1146038279, # BB
    1131472162, # Test
    1387645604, # Sam's
    292910019,  # Gwoop
    1144810801, # MC
}


# Check groups
@events.register(events.NewMessage(incoming=True,
                func=lambda e: not e.is_private))
async def check(event):
    if event.chat.id in whitelist:
        return

    res = await event.respond("Chat not in whitelist.  Leaving.")
    await event.client.kick_participant(event.chat, "me")

    await sleep(5)
    try:
        await event.client.delete_messages(
            event.chat, res
        )
    except errors.ChannelPrivateError:
        pass

    await log(event)    # Logs the event
