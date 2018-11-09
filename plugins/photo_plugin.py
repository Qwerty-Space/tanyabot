"""When an image file is sent to the bot, it will respond with a compressed preview of the file.
It will only respond to images under 10 MB.
"""

import os
from telethon import events, errors
from .global_functions import log


@events.register(events.NewMessage(outgoing=False))
async def on_photo(event):
    if event.message.sticker or not event.is_private:
        return
    try:
        msg = event.message
        image = msg.media.document
        mime_type = image.mime_type
    except AttributeError:
        return
    if "image" not in mime_type or image.size > 10000000:
        await event.reply("Image too large!  It must be under 10 MB.")
        await log(event, f"Image too large!")
        return
    file_name = f"{msg.from_id}{image.id}{msg.id}.{mime_type[+6:]}"
    await log(event, f"Image file: {file_name}")
    await event.download_media(file=file_name)
    try:
        await event.reply(file=file_name)
    except errors.rpcerrorlist.PhotoInvalidDimensionsError:
        await event.reply("The photo's dimensions are not supported by Telegram.")
    os.remove(f"{file_name}")
