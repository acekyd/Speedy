import logging
import datetime
import json
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
            return 0xc0dcfc
        case "Rare":
            return 0xf6e094
        case "Super Rare":
            return 0xd9b3ff
        case "Special":
            return 0x92f190


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

        items_button = [
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label=item,
                custom_id=item
            )
            for item in char_db[name_lower]['items']
        ]

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

        while True:
            res = await wait_for_component(
                self.client,
                components=items_button,
                messages=int(ctx.message.id),
                timeout=45,
            )

            projectiles_db = json.loads(open("./db/items-projectile.json", "r", encoding="utf8").read())

            if res.custom_id in projectiles_db:
                await res.send(f"{projectiles_db[res.custom_id]}")

            await res.send(f"Clicked! ID: {res.custom_id}")

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
