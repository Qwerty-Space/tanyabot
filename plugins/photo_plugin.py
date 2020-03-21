"""When an image file is sent to the bot, it will respond with a compressed preview of the file.
It will only respond to image files under 15 MB (15000000 bytes).
"""

import os
from PIL import Image
from io import BytesIO
from .global_functions import log
from telethon import events, errors, functions, types



async def downscale(item):
    im = Image.open(item)
    resolution = im.size
    size = 1280, 1280 # Rezise to a maxium of.  (Telegram's limit)
    outfile = BytesIO()

    im.thumbnail(size, Image.LANCZOS)
    im.save(outfile, "PNG")

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
    if image.size > 15 * 1000 * 1000: # 15 MB
        await event.reply("Image too large!  It must be under 15 MB.")
        await log(event, "Image too large!")
        return

    await log(event)

    async with event.client.action(event.from_id, "photo"):
        f = await event.download_media(file=BytesIO())
        f.seek(0)
        im, resolution = await downscale(f)
        im.seek(0)
        dimensions = f"`{resolution[0]}x{resolution[1]}`"

        try:
            im.name = "image.png"
            await event.reply(message=dimensions, file=im)
        except errors.rpcerrorlist.PhotoInvalidDimensionsError:
            await event.reply(f"The photo's dimensions ({dimensions}) are not supported by Telegram.")
