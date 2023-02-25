"""
/banner command.

(C) 2022-2023 - Jimmy-Blue
"""

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

    @interactions.slash_command(
        name="banner",
    )
    async def banner(self, ctx: interactions.SlashContext, **kwargs) -> None:
        """Banner related commands."""
        ...

    @banner.subcommand()
    @interactions.slash_option(
        name="event_name",
        description="The name of the event",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def event(
        self, ctx: interactions.SlashContext, event_name: str
    ) -> None:
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

        file = interactions.File(file=f"./db/event/{event_name}")
        title = (
            event_name.replace("banner_", "")
            .replace(".png", "")
            .replace("_", " ")
            .title()
        )
        embed = interactions.Embed(
            title=f"""{title[:-1] if title[-1].isdigit() else title}""",
            color=color,
            images=[
                interactions.EmbedAttachment(
                    url=f"attachment://{file.file_name}"
                )
            ],
        )
        await ctx.send(embeds=embed, file=file)

    @banner.subcommand()
    @interactions.slash_option(
        name="character_name",
        description="The name of the character",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def character(
        self, ctx: interactions.SlashContext, character_name: str
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

        file = interactions.File(file=f"./db/character/{character_name}")
        title = (
            character_name.replace("banner_", "")
            .replace(".png", "")
            .replace("_", " ")
            .title()
        )
        embed = interactions.Embed(
            title=f"""{title[:-1] if title[-1].isdigit() else title}""",
            color=color,
            images=[
                interactions.EmbedAttachment(
                    url=f"attachment://{file.file_name}"
                )
            ],
        )
        await ctx.send(embeds=embed, file=file)

    @event.autocomplete("event_name")
    async def event_autocomplete(
        self, ctx: interactions.AutocompleteContext
    ) -> None:
        """Autocomplete for /banner event command."""

        event_name: str = ctx.input_text
        if event_name != "":
            letters: list = event_name
        else:
            letters = []

        if len(event_name) == 0:
            await ctx.send(
                [
                    {
                        "name": str(self.banner_db[i])
                        .replace("banner_", "")
                        .replace(".png", "")
                        .replace("_", " ")
                        .title(),
                        "value": str(self.banner_db[i]),
                    }
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
                        {
                            "name": str(i)
                            .replace("banner_", "")
                            .replace(".png", "")
                            .replace("_", " ")
                            .title(),
                            "value": i,
                        }
                    )
            await ctx.send(choices)

    @character.autocomplete("character_name")
    async def character_autocomplete(
        self, ctx: interactions.AutocompleteContext
    ) -> None:
        """Autocomplete for /banner character command."""

        character_name: str = ctx.input_text
        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.send(
                [
                    {
                        "name": str(self.character_db[i])
                        .replace("banner_", "")
                        .replace(".png", "")
                        .replace("_", " ")
                        .title(),
                        "value": str(self.character_db[i]),
                    }
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
                        {
                            "name": str(i)
                            .replace("banner_", "")
                            .replace(".png", "")
                            .replace("_", " ")
                            .title(),
                            "value": i,
                        }
                    )
            await ctx.send(choices)
