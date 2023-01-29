import logging
import datetime
import os
import io
import interactions
from utils.colorthief import ColorThief


def get_color(img) -> str:
    """
    Get the dominant color of an image.
    :param img: The image.
    :type img:
    :return: The dominant color hex.
    :rtype: str
    """

    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)

    return dominant_color


class Banner(interactions.Extension):
    """Extension for /banner command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.banner_db = os.listdir("./db/event")
        self.character_db = os.listdir("./db/character")

    @interactions.extension_command(
        name="banner",
    )
    async def banner(self, ctx: interactions.CommandContext, **kwargs) -> None:
        """Banner related commands."""
        ...

    @banner.subcommand()
    @interactions.option("The name of the event", autocomplete=True)
    async def event(self, ctx: interactions.CommandContext, event_name: str) -> None:
        """Shows the banner of an event."""

        if event_name not in self.banner_db:
            return await ctx.send("Banner not found.", ephemeral=True)

        await ctx.defer()

        def clamp(x):
            return max(0, min(x, 255))

        with open(f"./db/event/{event_name}", "rb") as f:
            buf = io.BytesIO(f.read())

        color = get_color(buf)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)

        file = interactions.File(f"./db/event/{event_name}")
        embed = interactions.Embed(
            title=f"""{event_name.replace("banner_", "").replace(".png", "").replace("_", " ").title()}""",
            color=color,
            image=interactions.EmbedImageStruct(url=f"attachment://{file._filename}"),
        )
        await ctx.send(embeds=embed, files=file)

    @banner.subcommand()
    @interactions.option("The name of the character", autocomplete=True)
    async def character(
        self, ctx: interactions.CommandContext, character_name: str
    ) -> None:
        """Shows the banner of a character."""

        if character_name not in self.character_db:
            return await ctx.send("Character not found.", ephemeral=True)

        await ctx.defer()

        def clamp(x):
            return max(0, min(x, 255))

        with open(f"./db/character/{character_name}", "rb") as f:
            buf = io.BytesIO(f.read())

        color = get_color(buf)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)

        file = interactions.File(f"./db/character/{character_name}")
        embed = interactions.Embed(
            title=f"""{character_name.replace("banner_", "").replace(".png", "").replace("_", " ").title()}""",
            color=color,
            image=interactions.EmbedImageStruct(url=f"attachment://{file._filename}"),
        )
        await ctx.send(embeds=embed, files=file)

    @interactions.extension_autocomplete(command="banner", name="event_name")
    async def event_auto_complete(
        self, ctx: interactions.CommandContext, event_name: str = ""
    ) -> None:
        """Autocomplete for /banner event command."""

        if event_name != "":
            letters: list = event_name
        else:
            letters = []

        if len(event_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=str(self.banner_db[i])
                        .replace("banner_", "")
                        .replace(".png", "")
                        .replace("_", " ")
                        .title(),
                        value=str(self.banner_db[i]),
                    )
                    for i in range(0, 25)
                ]
            )
        else:
            choices: list = []
            for i in self.banner_db:
                focus: str = "".join(letters)
                if (
                    focus.lower()
                    in str(i)
                    .replace("banner_", "")
                    .replace(".png", "")
                    .replace("_", " ")
                    .lower()
                    and len(choices) < 20
                ):
                    choices.append(
                        interactions.Choice(
                            name=str(i)
                            .replace("banner_", "")
                            .replace(".png", "")
                            .replace("_", " ")
                            .title(),
                            value=i,
                        )
                    )
            await ctx.populate(choices)

    @interactions.extension_autocomplete(command="banner", name="character_name")
    async def character_auto_complete(
        self, ctx: interactions.CommandContext, character_name: str = ""
    ) -> None:
        """Autocomplete for /banner character command."""

        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=str(self.character_db[i])
                        .replace("banner_", "")
                        .replace(".png", "")
                        .replace("_", " ")
                        .title(),
                        value=str(self.character_db[i]),
                    )
                    for i in range(0, 25)
                ]
            )
        else:
            choices: list = []
            for i in self.character_db:
                focus: str = "".join(letters)
                if (
                    focus.lower()
                    in str(i)
                    .replace("banner_", "")
                    .replace(".png", "")
                    .replace("_", " ")
                    and len(choices) < 20
                ):
                    choices.append(
                        interactions.Choice(
                            name=str(i)
                            .replace("banner_", "")
                            .replace(".png", "")
                            .replace("_", " ")
                            .title(),
                            value=i,
                        )
                    )
            await ctx.populate(choices)


def setup(client) -> None:
    """Setup the extension."""

    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Banner(client)
    logging.debug("""[%s] Loaded Banner extension.""", log_time)
