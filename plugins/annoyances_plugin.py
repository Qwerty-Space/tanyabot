from telethon import events
from .global_functions import log
from telethon.tl.types import ChannelParticipantsAdmins

# Chats enabled:
chats = {-1001146038279, # BB
         -1001131472162, # Test
        }
# Banned content:
banned_bots = {306376942} # @nnbbot
banned_media = {"BAADAQADiwAD0r04RivkiZtrntB0Ag", # Stupid GIF Sky always sends 
                "BAADAgADLwUAAvNtEEjKi3Bn84YOSAI", # Other stupid GIF Sky always sends
               }

# Check for admins
admins = set()
async def check_admin(event):
    async for admin in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        admins.add(admin.id)


# Delete banned media
@events.register(events.NewMessage(
    func=lambda e: e.media and e.chat_id in chats
    ))
async def media_annoyances(event):
    if not admins:
        await check_admin(event)
    if event.from_id in admins:
        return

    if event.file.id not in banned_media:
        return

    await event.delete()
    await log(event)

# Delete banned bots
@events.register(events.NewMessage(
    func=lambda e: e.via_bot_id and e.chat_id in chats
    ))
async def bot_annoyances(event):
    if not admins:
        await check_admin(event)
    if event.from_id in admins:
        return

    if event.via_bot_id not in banned_bots:
        return

    await event.delete()
    await log(event)
