"""Slap 
"""
from random import choice
from telethon import events
from .global_functions import log, cooldown


async def random_slap(event, slapper, slapee):
    slap_list = [
        # Minecraft:
        f"{slapper} slapped {slapee}!",
        f"{slapee} walked into a cactus whilat trying to escape {slapper}",
        f"{slapee} was shot by an arrow",
        f"{slapee} was shot by {slapper}",
        f"{slapee} was roasted by {slapper}",
        f"{slapee} was roasted in dragon breath by {slapper}",
        f"{slapee} drowned by {slapper}",
        f"{slapee} was blown up by {slapper}",
        f"{slapee} fell from a high place",
        f"{slapee} was doomed to fall by {slapper}",
        f"{slapee} fell too far and was finished by {slapper}",
        f"{slapee} was squashed by a falling anvil",
        f"{slapee} was squashed by a falling anvil whilst fighting {slapper}",
        f"{slapee} went up in flames",
        f"{slapee} burned to death",
        f"{slapee} was burnt to a crisp whilst figting {slapper}",
        f"{slapee} went off with a bang",
        f"{slapee} went off with a bang whilst fighting {slapper}",
        f"{slapee} was slain by {slapper}",
        f"{slapee} got finished off by {slapper}",
        f"{slapee} was fireballed by {slapper}",
        f"{slapee} was killed by {slapper} using magic",
        f"{slapee} died",
        f"{slapee} fucking died", # Not Minecraft
        f"{slapee} died because of {slapper}",
        # Pokémon:
        f"{slapee} is out of usable Pokémon, {slapee} blacked out!",
        f"{slapee} is out of usable Pokémon, {slapee} whited out!",
        f"{slapee} lost against {slapper}, {slapee} blacked out!",
        f"{slapee} is blasting of again!",
        # Games:
        f"{slapee}'s mortality was clarified in a single strike",
        # Tech:
        f"{slapee} experienced a kernel panic",
        f"{slapee} was infected with malware from an email {slapper} sent them",
        f"{slapee} blue screened",
        # Memes:
        f"{slapee} was rickrolled",
        f"{slapee} triggered a feminazi",
        f"{slapee} is fresh out of lives",
        f"{slapee} shot John Wick's dog",
        f"{slapee} was introduced actual cannibal Shia Labeouf by {slapper}",
        # Animemes:
        f"{slapper}:  Omae wa mou shindeiru.\n{slapee}:  NANI?!",
        f"{slapee} was destroyed by {slapper}'s stand",
    ]
    return choice(slap_list)


@events.register(events.NewMessage(pattern=r"/slap(@\w+)?$"))
@cooldown(10)
async def slap(event):
    if not event.is_reply:
        return
    usr_group = event.pattern_match.group(1)
    username = (await event.client.get_me()).username
    if usr_group and username not in usr_group:
        return
    slapper = (await event.get_sender()).first_name
    slap_reply = await event.get_reply_message()
    slapee = await slap_reply.get_sender()
    mention_slapee = f"[{slapee.first_name}](tg://user?id={slapee.id})"
    await event.respond(await random_slap(event, slapper, mention_slapee))
