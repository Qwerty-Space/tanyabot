import re
import sys
import logging
import configparser
from importlib import import_module
from os import listdir, path
from datetime import datetime
from inspect import getmembers

from telethon import TelegramClient, custom, events, sync
from telethon.tl.types import (MessageEntityTextUrl, MessageEntityUrl,
                               MessageMediaDocument, MessageMediaPhoto)

logging.basicConfig(level=logging.INFO)
sys.dont_write_bytecode = True


### VARIABLES ###
config = configparser.ConfigParser()
config.read_file(open("config.ini"))
token = config['DEFAULT']['TOKEN']
session_name = config['DEFAULT']['SESSION_NAME']
api_id = config['DEFAULT']['ID']
api_hash = config['DEFAULT']['HASH']
superadmin = int(config['DEFAULT']['SUPERADMIN'])
script_dir = path.dirname(path.realpath(__file__))  # Set the location of the script


### LOG IN TO TELEGRAM ##
client = TelegramClient(path.join(script_dir, session_name), api_id, api_hash)


### IMPORT PLUGINS ###
plugindir = "plugins" # Change plugin path here
script_dir = path.dirname(path.realpath(__file__))
pluginfiles = listdir(plugindir)
plugin_dict = {}

for pluginfile in pluginfiles:
    if re.search(r".+plugin\.py$", pluginfile):
        plugin_name = pluginfile[:-3]
        plugin_shortname = plugin_name[:-7]
        plugin = import_module(f"plugins.{plugin_name}", plugin_name)
        plugin_dict[plugin_shortname] = plugin.__doc__
        for name, handler in getmembers(plugin):
            if events.is_handler(handler):
                client.add_event_handler(handler)


### HELP! ###
plugin_list = "`\n• `".join(plugin_dict)
help_message = f"""**List of commands:**
• `{plugin_list}`

Do `/help <command>` to learn more about it.
"""

@client.on(events.NewMessage(pattern=r"^/help(?: (\S+))?$"))
async def help(event):
    sender = await event.get_sender()
    if event.is_private:
        print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
        try:
            await event.respond(plugin_dict[event.pattern_match.group(1)], link_preview=False)
        except:
            await event.respond(help_message, link_preview=False)


client.start(bot_token=token)
try:
    client.send_message(superadmin, "**Bot started at:**  "+datetime.now().strftime("`%c`"))
except ValueError:
    pass

print("Bot started at:  "+datetime.now().strftime("%c"))
client.run_until_disconnected()
