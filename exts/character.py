import logging
import datetime
import json
import asyncio
import re
import interactions
from interactions.ext.wait_for import wait_for_component


def get_color(char_class: str):
    """
    Get the color hex based on the character class.

    :param class: The class of the player
    :type class: str
    :return: The color hex of the appropriate class.
    :rtype: str
    """
    match char_class:
        case "Common":
            return 0x96b1ca
        case "Rare":
            return 0xf9ab00
        case "Super Rare":
            return 0x8a32fb
        case "Special":
            return 0x12ad01
        case "Challenger":
            return 0xc92828


def create_bar(stat: str, num: int) -> str:

    green_bar: str = "<:bar_green:1045317811926466650>"
    red_bar: str = "<:bar_red:1045317809997090896>"
    bar_orange: str = "<:bar_orange:1045317805790212176>"
    bar_empty: str = "<:bar_empty:1045317807820242994>"

    match stat:
        case "speed":
            if 1 <= num <= 3:
                bar = num * red_bar
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 4 <= num <= 7:
                bar = num * bar_orange
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 8 <= num <= 10:
                bar = num * f"{green_bar}"
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
        case "acceleration":
            if 1 <= num <= 3:
                bar = num * red_bar
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 4 <= num <= 8:
                bar = num * bar_orange
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 9 <= num <= 10:
                bar = num * f"{green_bar}"
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
        case "strength":
            if 1 <= num <= 3:
                bar = num * red_bar
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 4 <= num <= 7:
                bar = num * bar_orange
                return f"{bar}" + ((10 - num) * f"{bar_empty}")
            elif 8 <= num <= 10:
                bar = num * f"{green_bar}"
                return f"{bar}" + ((10 - num) * f"{bar_empty}")


def get_emoji(emoji_str: str) -> tuple:
    """
    Returns the id/name of the emoji string in the message content.
    :param emoji_str: The emoji string.
    :type emoji_str: str
    :return: The ID of the emoji.
    :rtype: int
    """

    if (
        emoji_str.isnumeric() is False
        and emoji_str.startswith("<")
        and emoji_str.endswith(">")
    ):
        emoji_regex = re.compile(r"<?(a)?:(\w*):(\d*)>?")

        parsed = emoji_regex.findall(emoji_str)
        if parsed:
            parsed = tuple(filter(None, parsed[0]))
            if len(parsed) == 3:
                return (parsed[1], parsed[2], True)
            else:
                return (parsed[0], parsed[1], False)


class Character(interactions.Extension):
    """Extension for /character command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="character",
        description="Shows the information about a character.",
    )
    @interactions.option("The character you wish to search for.", autocomplete=True)
    async def _character(self, ctx: interactions.CommandContext, character_name: str):
        """Usage: /character [character_name]"""
        name_lower = character_name.lower()
        char_db = json.loads(open("./db/character.json", "r", encoding="utf8").read())
        if name_lower not in char_db:
            return await ctx.send("Character not found.", ephemeral=True)

        name = char_db[name_lower]["name"]
        color = get_color(char_db[name_lower]["rarity"])
        speed = char_db[name_lower]["speed"]
        acceleration = char_db[name_lower]["acceleration"]
        strength = char_db[name_lower]["strength"]
        rarity = char_db[name_lower]["rarity"]
        max_starting_rings = char_db[name_lower]["max_starting_rings"]
        image = char_db[name_lower]["image"]

        # items_button = [
        #     interactions.Button(
        #         style=interactions.ButtonStyle.SECONDARY,
        #         label=item,
        #         emoji=interactions.Emoji(id=get_emoji()),
        #         custom_id=item
        #     )
        #     for item in char_db[name_lower]['items']
        # ]

        items_button, cnt = [], 0
        for item in char_db[name_lower]['items']:
            if cnt == 0:
                projectile_db = json.loads(open("./db/items-projectile.json", "r", encoding="utf8").read())
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        emoji=interactions.Emoji(id=get_emoji(projectile_db[item]["emoji"])[1]),
                        custom_id=item
                    )
                )
                cnt += 1
            elif cnt == 1:
                boost_db = json.loads(open("./db/items-boost.json", "r", encoding="utf8").read())
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        emoji=interactions.Emoji(id=get_emoji(boost_db[item]["emoji"])[1]),
                        custom_id=item
                    )
                )
                cnt += 1
            else:
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        custom_id=item
                    )
                )

        embed = interactions.Embed(
            title=name,
            description="".join(
                [
                    f"Rarity: {rarity}\n",
                    f"Max Starting Rings: {max_starting_rings}\n",
                    f"Total Stats: {speed + acceleration + strength}"
                ]
            ),
            color=color,
            thumbnail=interactions.EmbedImageStruct(url=image)
        )
        embed.add_field(name=f"Speed: {speed}/10", value=create_bar("speed", speed))
        embed.add_field(name=f"Acceleration: {acceleration}/10", value=create_bar("acceleration", acceleration))
        embed.add_field(name=f"Strength: {strength}/10", value=create_bar("strength", strength))

        await ctx.send(embeds=embed, components=items_button)

        try:
            while True:
                res = await wait_for_component(
                    self.client,
                    components=items_button,
                    messages=int(ctx.message.id),
                    timeout=45,
                )
                index = [btn.custom_id for btn in items_button].index(res.custom_id)
                match index:
                    case 0:
                        projectile_db = json.loads(open("./db/items-projectile.json", "r", encoding="utf8").read())
                        embed = interactions.Embed(
                            title=str(res.custom_id),
                            description="".join(
                                [
                                    f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["description", "image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n""" for k, v in list(projectile_db[str(res.custom_id)].items())
                                ]
                            ),
                            image=interactions.EmbedImageStruct(url=str(projectile_db[str(res.custom_id)]["image"]))
                        )
                        await res.send(embeds=embed)
                    case 1:
                        boost_db = json.loads(open("./db/items-boost.json", "r", encoding="utf8").read())
                        embed = interactions.Embed(
                            title=str(res.custom_id),
                            description="".join(
                                [
                                    f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["description", "image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n""" for k, v in list(boost_db[str(res.custom_id)].items())
                                ]
                            ),
                            image=interactions.EmbedImageStruct(url=str(boost_db[str(res.custom_id)]["image"]))
                        )
                        await res.send(embeds=embed)
                    case 2:
                        trap_db = json.loads(open("./db/items-trap.json", "r", encoding="utf8").read())
                        embed = interactions.Embed(
                            title=str(res.custom_id),
                            description="".join(
                                [
                                    f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n""" for k, v in list(trap_db[str(res.custom_id)].items())
                                ]
                            ),
                        )
                        await res.send(embeds=embed)

        except asyncio.TimeoutError:
            pass

    @interactions.extension_autocomplete(command="character", name="character_name")
    async def auto_complete(
        self, ctx: interactions.CommandContext, character_name: str = ""
    ):
        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        db = json.loads(open("./db/character.json", "r", encoding="utf8").read())

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=db[name]['name'], value=name
                    )
                    for name in (
                        list(db.keys())[0:9]
                        if len(db) > 10
                        else list(db.keys())
                    )
                ]
            )
        else:
            choices: list = []
            for char_name in db:
                focus: str = "".join(letters)
                if focus.lower() in char_name and len(choices) < 20:
                    choices.append(
                        interactions.Choice(
                            name=db[char_name]['name'], value=char_name
                        )
                    )
            await ctx.populate(choices)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Character(client)
    logging.debug("""[%s] Loaded About extension.""", log_time)
