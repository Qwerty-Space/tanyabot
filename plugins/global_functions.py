import time
import asyncio
import inspect
import logging
from PIL import Image
from io import BytesIO
from random import random
from collections import defaultdict


# Probability
def probability(percent):
    outcome = random() < percent
    return outcome

# Logging
async def log(event, info=""):
    sender = await event.get_sender()
    # Get the name of the command sent to the bot:
    command = inspect.currentframe().f_back.f_code.co_name
    logging.info(
        f"""[{event.date.strftime('%c')}]:
    [{sender.id}]@[{event.chat_id}] {sender.first_name}@{sender.username}: {command}
    {info}""".rstrip())

# Cooldown
def cooldown(timeout):
    def wrapper(function):
        last_called = defaultdict(int)

        async def wrapped(event, *args, **kwargs):
            current_time = time.time()
            if current_time - last_called[event.chat_id] < timeout:
                time_left = round(timeout - (current_time - last_called[event.chat_id]), 1)
                await log(event, f"Cooldown: {time_left}s")
                return
            last_called[event.chat_id] = current_time
            return await function(event, *args, **kwargs)
        return wrapped
    return wrapper

async def downscale(item, x=1280, y=1280, format="PNG"):
    im = Image.open(item)
    resolution = im.size
    size = x, y # Rezise to a maxium of.  (Telegram's limit)
    outfile = BytesIO()

    im.thumbnail(size, Image.LANCZOS)
    im.save(outfile, format)

    return outfile, resolution
