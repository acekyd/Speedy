import logging
import datetime
import json
import interactions


def get_color(char_class: str):
    """
    Get the color hex based on the character class.

    :param class: The class of the player
    :type class: str
    :return: The color hex of the appropriate class.
    :rtype: str
    """
    match char_class:
        case 'Common':
            return 0xc0dcfc


def create_bar(num: int) -> str:

    green_bar: str = "<:bar_green:1045317811926466650>"
    red_bar: str = "<:bar_red:1045317809997090896>"
    bar_orange: str = "<:bar_orange:1045317805790212176>"
    bar_empty: str = "<:bar_empty:1045317807820242994>"

    if 1 <= num <= 5:
        bar = num * red_bar
        return f"{bar}" + ((10 - num) * f"{bar_empty}")
    elif 6 <= num <= 9:
        bar = num * bar_orange
        return f"{bar}" + ((10 - num) * f"{bar_empty}")
    elif num == 10:
        return 10 * f"{green_bar}"


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
        db = json.loads(open("./db/character.json", "r", encoding="utf8").read())
        if name_lower not in db:
            return await ctx.send("Character not found.", ephemeral=True)

        name = db[name_lower]["name"]
        color = get_color(db[name_lower]["rarity"])
        speed = db[name_lower]["speed"]
        acceleration = db[name_lower]["acceleration"]
        strength = db[name_lower]["strength"]
        rarity = db[name_lower]["rarity"]
        max_starting_rings = db[name_lower]["max_starting_rings"]
        image = db[name_lower]["image"]

        items_button = [
            interactions.Button(
                style=interactions.ButtonStyle.SECONDARY,
                label=item,
                custom_id=item.lower().replace(" ", "_")
            )
            for item in db[name_lower]['items']
        ]

        embed = interactions.Embed(
            title=name,
            description="".join(
                [
                    f"Rarity: {rarity}\n",
                    f"Max Starting Rings: {max_starting_rings}",
                ]
            ),
            color=color,
            thumbnail=interactions.EmbedImageStruct(url=image)
        )
        embed.add_field(name=f"Speed: {speed}/10", value=create_bar(speed))
        embed.add_field(name=f"Acceleration: {acceleration}/10", value=create_bar(acceleration))
        embed.add_field(name=f"Strength: {strength}/10", value=create_bar(strength))

        await ctx.send(embeds=embed, components=items_button)

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
