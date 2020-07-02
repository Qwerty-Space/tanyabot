"""Downloads SFW `v.reddi.it` videos, and sends them back as a video.
"""

import os
import string
import requests
import subprocess
import youtube_dl
from time import time
from ffmpy import FFmpeg
from random import randint, choice

import re
from telethon import events
from .global_functions import log, downscale


ytdl_opts = {
    "format": "best/bestvideo+bestaudio",
    "quiet": "true"
}

async def generator(size=randint(8,16)):
    chars = string.ascii_letters + string.digits
    return "".join(choice(chars) for _ in range(size))


async def vreddit(event, match):
    vids = []

    check = await event.reply(f"Checking")
    for m in match:
        await check.edit(f"Checking {match.index(m)+1}/{len(match)}")
        url = requests.get(m).url
        post_json = requests.get(url + ".json", headers={'User-Agent': f"{await generator()}"}).json()
        over_18 = post_json[0]['data']['children'][0]['data']['over_18']

        if over_18 and event.is_private or not over_18:
            vids.append(m)
        elif over_18 and not event.is_private:
            me = (await event.client.get_me()).username
            sub = re.sub(r"(?:https?\://)?v\.redd\.it/", "", m)

            link = f"t.me/{me}?start=vreddit_{sub}"
            await event.reply(f"[NSFW: click to view]({link})", link_preview=False)

    await check.delete()
    await log(event)

    for v in vids:
        dl_msg = await event.reply(f"Downloading... {match.index(v)+1}/{len(vids)}")

        try:
            now = str(time())
            ytdl_opts["outtmpl"] = f"%(title)s{now}.%(ext)s"
            with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
                f = ytdl.extract_info(v)

            file_name = f"{f['title']}{now}.mp4"
            outfile = "o_" + file_name
            thumbbig = outfile + ".jpg"

            ff = FFmpeg(
                inputs={file_name: None},
                outputs={
                    outfile: "-c:v libx264 -pix_fmt yuv420p -b:v 3M -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2'",
                    thumbbig: "-ss 00:00:01.000 -vframes 1"
                }
            )
            ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            # ff.run()
            thumb, res = await downscale(thumbbig, 100, 100, format="JPEG")
            thumb.seek(0)

            async with event.client.action(event.chat, "video"):
                thumb.name = "image.jpg"
                # TODO:
                ## Get thumbnails working - i have no idea how
                await event.client.send_file(event.chat_id, file=outfile, caption=v, reply_to=event.id, thumb=thumb, supports_streaming=True)
        except:
            pass

        await dl_msg.delete()
        os.remove(file_name)
        os.remove(outfile)
        os.remove(thumbbig)



@events.register(events.NewMessage(pattern=r"/start vreddit_(\w+)$"))
async def on_start_vid(event):
    link = ["https://v.redd.it/" + event.pattern_match.group(1)]
    await vreddit(event, link)


@events.register(events.NewMessage(pattern=re.compile(
                                    r"(?i)(?:^|\s)((?:https?\://)?v\.redd\.it/\w+)").findall
                                    ))
async def on_vreddit(event):
    # Check if the message is forwarded from self
    fwd = event.forward

    if fwd and (await fwd.get_sender()).is_self:
        return
    else:
        await vreddit(event, event.pattern_match)

