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


class Wallpaper(interactions.Extension):
    """Extension for /wallpaper command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.wallpaper_db = os.listdir("./db/wallpaper")

    @interactions.extension_command()
    @interactions.option("The name of the wallpaper", autocomplete=True)
    async def wallpaper(
        self, ctx: interactions.CommandContext, wallpaper_name: str
    ) -> None:
        """Shows the wallpaper of an event/character."""
        await ctx.defer()

        def clamp(x):
            return max(0, min(x, 255))

        with open(f"./db/wallpaper/{wallpaper_name}", "rb") as f:
            buf = io.BytesIO(f.read())

        color = get_color(buf)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)

        if wallpaper_name not in self.wallpaper_db:
            return await ctx.send("Banner not found.", ephemeral=True)

        file = interactions.File(f"./db/wallpaper/{wallpaper_name}")
        embed = interactions.Embed(
            title=f"""{wallpaper_name.replace("banner_", "").replace(".png", "").replace("_", " ").title()}""",
            color=color,
            image=interactions.EmbedImageStruct(url=f"attachment://{file._filename}"),
        )
        await ctx.send(embeds=embed, files=file)

    @interactions.extension_autocomplete(command="wallpaper", name="wallpaper_name")
    async def wallpaper_auto_complete(
        self, ctx: interactions.CommandContext, wallpaper_name: str = ""
    ):
        if wallpaper_name != "":
            letters: list = wallpaper_name
        else:
            letters = []

        if len(wallpaper_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=str(self.wallpaper_db[i])
                        .replace("wallpaper_", "")
                        .replace(".png", "")
                        .replace("_", " ")
                        .title(),
                        value=str(self.wallpaper_db[i]),
                    )
                    for i in range(0, 25)
                ]
            )
        else:
            choices: list = []
            for i in self.wallpaper_db:
                focus: str = "".join(letters)
                if (
                    focus.lower()
                    in str(i)
                    .replace("wallpaper_", "")
                    .replace(".png", "")
                    .replace("_", " ")
                    .lower()
                    and len(choices) < 20
                ):
                    choices.append(
                        interactions.Choice(
                            name=str(i)
                            .replace("wallpaper_", "")
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
    Wallpaper(client)
    logging.debug("""[%s] Loaded Wallpaper extension.""", log_time)
