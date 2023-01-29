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


class RunnerReport(interactions.Extension):
    """Extension for /runnerreport command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.report_db = os.listdir("./db/runnerreport")

    @interactions.extension_command()
    @interactions.option("The name of the character", autocomplete=True)
    async def runnerreport(
        self, ctx: interactions.CommandContext, character_name: str
    ) -> None:
        """Shows the image of a character from Runner Report."""

        if character_name not in self.report_db:
            return await ctx.send("Image not found.", ephemeral=True)

        await ctx.defer()

        def clamp(x):
            return max(0, min(x, 255))

        with open(f"./db/runnerreport/{character_name}", "rb") as f:
            buf = io.BytesIO(f.read())

        color = get_color(buf)
        color = "#{0:02x}{1:02x}{2:02x}".format(
            clamp(color[0]), clamp(color[1]), clamp(color[2])
        )
        color = str("0x" + color[1:])
        color = int(color, 16)

        file = interactions.File(f"./db/runnerreport/{character_name}")
        embed = interactions.Embed(
            title=f"""{character_name.replace("runner_report_", "").replace(".jpg", "").replace("_", " ").title()}""",
            color=color,
            image=interactions.EmbedImageStruct(url=f"attachment://{file._filename}"),
        )
        await ctx.send(embeds=embed, files=file)

    @interactions.extension_autocomplete(command="runnerreport", name="character_name")
    async def image_auto_complete(
        self, ctx: interactions.CommandContext, character_name: str = ""
    ) -> None:
        """Autocomplete for /runnerreport command."""

        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(
                        name=str(self.report_db[i])
                        .replace("runner_report_", "")
                        .replace(".jpg", "")
                        .replace("_", " ")
                        .title(),
                        value=str(self.report_db[i]),
                    )
                    for i in range(0, 10)
                ]
            )
        else:
            choices: list = []
            for i in self.report_db:
                focus: str = "".join(letters)
                if (
                    focus.lower()
                    in str(i)
                    .replace("runner_report_", "")
                    .replace(".jpg", "")
                    .replace("_", " ")
                    .lower()
                    and len(choices) < 20
                ):
                    choices.append(
                        interactions.Choice(
                            name=str(i)
                            .replace("runner_report_", "")
                            .replace(".jpg", "")
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
    RunnerReport(client)
    logging.debug("""[%s] Loaded RunnerReport extension.""", log_time)
