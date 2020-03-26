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


async def vreddit(event, match):
    vids = []
    if event.is_private:
        chat = event.from_id
    else:
        chat = event.to_id

    check = await event.reply(f"Checking")
    for m in match:
        await check.edit(f"Checking {match.index(m)+1}/{len(match)}")
        url = requests.get(m).url
        post_json = requests.get(url + ".json", headers={'User-Agent': f"{randint(10000,99999)}"}).json()
        over_18 = post_json[0]['data']['children'][0]['data']['over_18']

        if over_18 and event.is_private or not over_18:
            vids.append(m)
        elif over_18 and not event.is_private:
            me = (await event.client.get_me()).username
            sub = re.sub(r"(?:https?\://)?v\.redd\.it/", "", m)

            link = f"t.me/{me}?start=vreddit_{sub}"
            await event.reply(f"[NSFW: click to view]({link})")

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
            # thumb = final_file + ".jpg"

            ff = FFmpeg(
                inputs={file_name: None},
                outputs={
                    final_file: "-c:v libx264 -pix_fmt yuv420p -b:v 3M -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2'",
                    # thumb: "-ss 00:00:01.000 -vframes 1"
                }
            )
            ff.run(stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            # await event.client.send_file(event.from_id, final_file,
            #                             caption=v, reply_to=event.message,
            #                             supports_streaming=True, thumb=thumb)
            async with event.client.action(chat, "video"):
                await event.reply(v, file=final_file)
        except:
            pass

        await dl_msg.delete()
        os.remove(file_name)
        # os.remove(thumb)
        os.remove(final_file)



@events.register(events.NewMessage(pattern=r"/start vreddit_(\w+)$"))
async def on_start_vid(event):
    link = ["https://v.redd.it/" + event.pattern_match.group(1)]
    await download(event, link)


@events.register(events.NewMessage(pattern=re.compile(
                                    r"(?i)(?:^|\s)((?:https?\://)?v\.redd\.it/\w+)").findall
                                    ))
async def on_vreddit(event):
        await download(event, event.pattern_match)

