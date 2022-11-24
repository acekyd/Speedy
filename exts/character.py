import logging
import datetime
import json
import interactions
from interactions.ext import molter


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


class Character(molter.MolterExtension):
    """Extension for /character command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="character",
        description="Shows the information about a character.",
    )
    @interactions.option("The character you wish to search for.", required=True, autocomplete=True)
    async def _character(self, ctx: interactions.CommandContext, character_name: str):
        """Usage: /character [character_name]"""
        name_lower = character_name.lower()
        db = json.loads(open("./db/character.json", "r", encoding="utf8").read())
        if name_lower not in db:
            return await ctx.send("Character not found.", ephemeral=True)

        name = db[name_lower]["name"]
        color = get_color(db[name_lower]['class'])
        speed = db[name_lower]['speed']
        acceleration = db[name_lower]['acceleration']
        strength = db[name_lower]['strength']
        image = db[name_lower]['image']
        items = "\n".join(item for item in db[name_lower]['items'])

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
            color=color,
            thumbnail=interactions.EmbedImageStruct(url=image)
        )
        embed.add_field(name="Stats", value=f"Speed: {speed}\nAcceleration: {acceleration}\nStrength: {strength}", inline=True)
        embed.add_field(name="Items", value=items, inline=True)

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