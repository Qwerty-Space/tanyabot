"""When an image file is sent to the bot, it will respond with a compressed preview of the file.
It will only respond to image files under 15 MB (15000000 bytes).
"""

import os
from PIL import Image
from telethon import events, errors, functions, types
from .global_functions import log


async def downscale(item):
    im = Image.open(item)
    resolution = im.size
    size = 1280, 1280 # Rezise to a maxium of.  (Telegram's limit)
    outfile = f"{item}.thumb.{im.format}"

    im.thumbnail(size, Image.LANCZOS)
    im.save(outfile)

    return outfile, resolution


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
    if "image" not in mime_type:
        return
    if image.size > 15000000: # 15 MB
        await event.reply("Image too large!  It must be under 15 MB.")
        await log(event, "Image too large!")
        return

    notification = await event.reply("Loading...")
    print(notification)
    file_name = f"{msg.from_id}{image.id}{msg.id}.{mime_type[+6:]}"
    await log(event, f"Image file: {file_name}")

    await event.client(functions.messages.SetTypingRequest(
        peer=event.from_id,
        action=types.SendMessageUploadPhotoAction(1)
    ))

    await event.download_media(file=file_name)
    im, resolution = await downscale(file_name)
    dimensions = f"`{resolution[0]}x{resolution[1]}`"
    os.remove(file_name)

    try:
        await event.reply(message=dimensions, file=im)
    except errors.rpcerrorlist.PhotoInvalidDimensionsError:
        await event.reply(f"The photo's dimensions ({dimensions}) are not supported by Telegram.")
    await event.client.delete_messages(entity=None, message_ids=notification)
    os.remove(im)
