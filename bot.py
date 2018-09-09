import re
import sys
import logging
import configparser
from os import listdir, path
from datetime import datetime
from inspect import getmembers

from telethon import TelegramClient, custom, events, sync
from telethon.tl.types import (MessageEntityTextUrl, MessageEntityUrl,
                               MessageMediaDocument, MessageMediaPhoto)

logging.basicConfig(level=logging.WARNING)


### VARIABLES ###
config = configparser.ConfigParser()
config.read_file(open("config.ini"))
token = config['DEFAULT']['TOKEN']
session_name = config['DEFAULT']['SESSION_NAME']
api_id = config['DEFAULT']['ID']
api_hash = config['DEFAULT']['HASH']
superadmin = int(config['DEFAULT']['superadmin'])
script_dir = path.dirname(path.realpath(__file__))  # Set the location of the script


### LOG IN TO TELEGRAM ##
print("Connecting...")
client = TelegramClient(path.join(script_dir, session_name), api_id, api_hash)


### IMPORT PLUGINS ###
plugindir = "plugins"
script_dir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(script_dir, plugindir))
pluginfiles = listdir(plugindir)

for pluginfile in pluginfiles:
    if re.search(r".+plugin\.py$", pluginfile):
        plugin_name = f"{pluginfile}"[:-3]
        plugin = __import__(f"{plugin_name}", globals(), locals(), [], 0)
        for name, handler in getmembers(plugin):
            if hasattr(handler, 'event'):
                client.add_event_handler(handler, handler.event)


### TESTING ###
# Send as photo
# @client.on(events.NewMessage)
# async def lazy_download(event):
#     # sender = await event.get_sender()
#     # print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
#     print(f"\n\n\nSTRINGIFY!\n\n\n{event.entities()}")
#     if any(isinstance(x, (MessageMediaDocument)) for x in event. or []):
#         event.reply(types.MessageMediaPhoto)


client.start(bot_token=token)

try:
    client.send_message(superadmin, "**Bot started at:**  "+datetime.now().strftime("`%c`"))
except ValueError:
    pass

print("Bot started at:  "+datetime.now().strftime("%c"))
client.run_until_disconnected()
