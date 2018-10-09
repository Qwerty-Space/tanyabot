"""NOT WORKING
Respond with a link to a Pokémon etc.
"""

from telethon import events, sync
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen
import re

# Pokédex
@events.register(events.NewMessage(pattern=re.compile(r"^(?:pok[eé]mon|pok[eé]dex|bulba(?:pedia|garden)) (.+)$", re.I)))
async def pokedex(event):
    sender = await event.get_sender()
    search_term = urlencode({"q" : event.pattern_match.group(1)})
    html_content = urlopen(f"https://pokemondb.net/search?{search_term}")
    search_results = re.findall(r'q=https://pokemondb\.net/(\w+/[\w-]+)', html_content.read().decode())
    # search_term = re.sub(r" ", "+", event.pattern_match.group(1))
    print(f"[{event.date.strftime('%c')}] [{sender.id}] {sender.username}: {event.pattern_match.string}")
    message = await event.reply(urljoin("https://pokemondb.net/", search_results.group(1)))
    print(message)
