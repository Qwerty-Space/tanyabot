"""Generates fancy colours by abusing the order(lessness) of a set.
Based on [ass.py, by udf](https://gist.github.com/udf/c452669e251f8f5507555e3b7826a432).

Has a per-chat cooldown of 5 minutes.

pattern:  `/ass(@bots_username)?$`
"""
import os
import time
from PIL import Image
from telethon import events
from .global_functions import log, cooldown
from random import randint, getrandbits


def thing(val):
    val += (-7, -3, -2, -1, 5, 2, 3, 4)[getrandbits(3)]
    if val < 0: return 0
    if val > 255: return 255
    return val


def neighbours(coord, w, h):
    offsets = ((1, 0), (-1, 0), (1, 1), (0, 1), (0, -1), (-1, -1), (1, 0), (1, -1))
    for xo, yo in offsets:
        nx = coord[0] + xo
        ny = coord[1] + yo
        if nx >= 0 and nx < w and ny >= 0 and ny < h:
            yield nx, ny

@events.register(events.NewMessage(pattern=r"/ass(@\w+)?$"))
@cooldown(300)
async def send_ass(event):
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return
    wait_msg = await event.reply("Generating...  Please wait approximately 10 seconds")
    await log(event, "Generating")
    start_time = round(time.time(), 2)
    msg = event.message
    file_name = f"ass_{msg.from_id}_{start_time}.png"
    w = 512
    h = 512
    x_origin = randint(0, w)
    y_origin = randint(0, h)
    randr = randint(0, 255)
    randg = randint(0, 255)
    randb = randint(0, 255)
    im = Image.new('RGB', (w, h))

    done = set()
    pending = set()
    pending.add((randr, randg, randb, (x_origin, y_origin))) # (R, G, B, (x, y)) changes the colour, and origin pixel

    n_iters = 0
    while pending:
        # if n_iters % 10000 == 0: # Debugging
        #     print(len(done))

        r, g, b, dest = pending.pop()

        r = thing(r)
        g = thing(g)
        b = thing(b)

        im.putpixel(dest, (r, g, b))
        done.add(dest)
        n_iters += 1

        for neighbour in neighbours(dest, w, h):
            if neighbour not in done:
                pending.add((r, g, b, neighbour))

    im.save(file_name)
    delta_time = round(time.time() - start_time, 2)
    await event.reply(f"Took {delta_time} seconds", file=file_name)
    await wait_msg.delete()
    await log(event, f"Finished.  Took {delta_time} seconds")
    os.remove(file_name)
