"""Downloads SFW `v.reddi.it` videos, and sends them back as a video.
"""

import os
import requests
import subprocess
import youtube_dl
from ffmpy import FFmpeg
from time import time
from random import randint

import re
from telethon import events
from .global_functions import log

ytdl_opts = {
    "format": "best/bestvideo+bestaudio",
    "quiet": "true"
}


@events.register(events.NewMessage(pattern=re.compile(
                                    r"(?i)(?:^|\s)((?:https?\://)?v\.redd\.it/\w+)").findall
                                    ))
async def vreddit(event):
    match = event.pattern_match
    vids = []
    check = await event.reply(f"Checking")
    for m in match:
        await check.edit(f"Checking {match.index(m)+1}/{len(match)}")
        url = requests.get(m).url
        post_json = requests.get(url + ".json", headers={'User-Agent': f"{randint(10000,99999)}"}).json()
        over_18 = post_json[0]['data']['children'][0]['data']['over_18']

        if not over_18:
            vids.append(m)

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
            final_file = "o_" + file_name
            thumb = final_file + ".jpg"

            ff = FFmpeg(
                inputs={file_name: None},
                outputs={
                    final_file: "-c:v libx264 -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2'",
                    thumb: "-ss 00:00:01.000 -vframes 1"
                }
            )
            ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            await event.client.send_file(event.from_id, final_file,
                                        caption=v, reply_to=event.message,
                                        supports_streaming=True, thumb=thumb)
        except:
            pass

        await dl_msg.delete()
        os.remove(file_name)
        os.remove(thumb)
        os.remove(final_file)

