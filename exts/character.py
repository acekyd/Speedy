import logging
import datetime
import json
import asyncio
import re
import interactions
from interactions.ext.wait_for import wait_for_component


def get_color(char_class: str) -> int:
    """
    Get the color hex based on the character class.

    :param class: The class of the player
    :type class: str
    :return: The color hex of the appropriate class.
    :rtype: int
    """

    if char_class == "Common":
        return 0x96B1CA
    elif char_class == "Rare":
        return 0xF9AB00
    elif char_class == "Super Rare":
        return 0x8A32FB
    elif char_class == "Special":
        return 0x12AD01
    elif char_class == "Challenger":
        return 0xC92828


def create_bar(stat: str, num: int) -> str:

    green_bar: str = "<:bar_green:1045317811926466650>"
    red_bar: str = "<:bar_red:1045317809997090896>"
    bar_orange: str = "<:bar_orange:1045317805790212176>"
    bar_empty: str = "<:bar_empty:1045317807820242994>"

    if stat == "speed":
        if 1 <= num <= 3:
            bar = num * red_bar
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
        elif 4 <= num <= 7:
            bar = num * bar_orange
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
        elif 8 <= num <= 10:
            bar = num * f"{green_bar}"
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
    elif stat == "acceleration":
        if 1 <= num <= 3:
            bar = num * red_bar
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
        elif 4 <= num <= 8:
            bar = num * bar_orange
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
        elif 9 <= num <= 10:
            bar = num * f"{green_bar}"
            return f"{bar}" + ((10 - num) * f"{bar_empty}")
    elif stat == "strength":
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
        self.char_db = json.loads(
            open("./db/character.json", "r", encoding="utf8").read()
        )
        self.projectile_db = json.loads(
            open("./db/items-projectile.json", "r", encoding="utf8").read()
        )
        self.boost_db = json.loads(
            open("./db/items-boost.json", "r", encoding="utf8").read()
        )
        self.trap_db = json.loads(
            open("./db/items-trap.json", "r", encoding="utf8").read()
        )

    @interactions.extension_command(
        name="character",
        description="Shows the information about a character.",
    )
    @interactions.option("The character you wish to search for.", autocomplete=True)
    async def _character(self, ctx: interactions.CommandContext, character_name: str):
        """Usage: /character [character_name]"""

        name_lower = character_name.lower()

        if name_lower not in self.char_db:
            return await ctx.send("Character not found.", ephemeral=True)

        name = self.char_db[name_lower]["name"]
        color = get_color(self.char_db[name_lower]["rarity"])
        speed = self.char_db[name_lower]["speed"]
        acceleration = self.char_db[name_lower]["acceleration"]
        strength = self.char_db[name_lower]["strength"]
        rarity = self.char_db[name_lower]["rarity"]
        max_starting_rings = self.char_db[name_lower]["max_starting_rings"]
        image = self.char_db[name_lower]["image"]

        items_button, cnt = [], 0
        for item in self.char_db[name_lower]["items"]:
            if cnt == 0:
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        emoji=interactions.Emoji(
                            id=get_emoji(self.projectile_db[item]["emoji"])[1]
                        ),
                        custom_id=item,
                    )
                )
                cnt += 1
            elif cnt == 1:
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        emoji=interactions.Emoji(
                            id=get_emoji(self.boost_db[item]["emoji"])[1]
                        ),
                        custom_id=item,
                    )
                )
                cnt += 1
            elif cnt == 2:
                items_button.append(
                    interactions.Button(
                        style=interactions.ButtonStyle.SECONDARY,
                        label=item,
                        emoji=interactions.Emoji(
                            id=get_emoji(self.trap_db[item]["emoji"])[1]
                        ),
                        custom_id=item,
                    )
                )

        embed = interactions.Embed(
            title=name,
            description="".join(
                [
                    f"Rarity: {rarity}\n",
                    f"Max Starting Rings: {max_starting_rings}\n",
                    f"Total Stats: {speed + acceleration + strength}",
                ]
            ),
            color=color,
            thumbnail=interactions.EmbedImageStruct(url=image),
        )
        embed.add_field(name=f"Speed: {speed}/10", value=create_bar("speed", speed))
        embed.add_field(
            name=f"Acceleration: {acceleration}/10",
            value=create_bar("acceleration", acceleration),
        )
        embed.add_field(
            name=f"Strength: {strength}/10", value=create_bar("strength", strength)
        )

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
                if index == 0:
                    embed = interactions.Embed(
                        title=str(res.custom_id),
                        description="".join(
                            [
                                f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["description", "image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n"""
                                for k, v in list(
                                    self.projectile_db[str(res.custom_id)].items()
                                )
                            ]
                        ),
                        image=interactions.EmbedImageStruct(
                            url=str(self.projectile_db[str(res.custom_id)]["image"])
                        ),
                    )
                elif index == 1:
                    embed = interactions.Embed(
                        title=str(res.custom_id),
                        description="".join(
                            [
                                f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["description", "image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n"""
                                for k, v in list(
                                    self.boost_db[str(res.custom_id)].items()
                                )
                            ]
                        ),
                        image=interactions.EmbedImageStruct(
                            url=str(self.boost_db[str(res.custom_id)]["image"])
                        ),
                    )
                elif index == 2:
                    embed = interactions.Embed(
                        title=str(res.custom_id),
                        description="".join(
                            [
                                f"""{k.capitalize().replace("_", " ") + ": " if str(k) not in ["description", "image", "emoji"] else ""}{"✅" if type(v) == bool and bool(v) == True else ("❌" if type(v) == bool and bool(v) == False else (v if str(v).startswith(("https", "<:")) is False else ""))}\n"""
                                for k, v in list(
                                    self.trap_db[str(res.custom_id)].items()
                                )
                            ]
                        ),
                        image=interactions.EmbedImageStruct(
                            url=str(self.trap_db[str(res.custom_id)]["image"])
                        ),
                    )
                await res.send(embeds=embed, ephemeral=True)

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

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(name=self.char_db[name]["name"], value=name)
                    for name in (
                        list(self.char_db.keys())[0:9]
                        if len(self.char_db) > 10
                        else list(self.char_db.keys())
                    )
                ]
            )
        else:
            choices: list = []
            for char_name in self.char_db:
                focus: str = "".join(letters)
                if focus.lower() in char_name.lower() and len(choices) < 20:
                    choices.append(
                        interactions.Choice(
                            name=self.char_db[char_name]["name"], value=char_name
                        )
                    )
            await ctx.populate(choices)


def setup(client) -> None:
    """Setup the extension."""

    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Character(client)
    logging.debug("""[%s] Loaded Character extension.""", log_time)
