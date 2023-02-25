"""
/runnerreport command.

(C) 2023 - Jimmy-Blue
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


class RunnerReport(interactions.Extension):
    """Extension for /runnerreport command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.report_db = os.listdir("./db/runnerreport")

    @interactions.slash_command()
    @interactions.slash_option(
        name="character_name",
        description="The name of the character",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    async def runnerreport(
        self, ctx: interactions.SlashContext, character_name: str
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

        file = interactions.File(file=f"./db/runnerreport/{character_name}")
        embed = interactions.Embed(
            title=f"""{(
                character_name
                .replace("runner_report_", "")
                .replace(".jpg", "")
                .replace("_", " ")
                .title()
            )}""",
            color=color,
            images=[
                interactions.EmbedAttachment(
                    url=f"attachment://{file.file_name}"
                )
            ],
        )
        await ctx.send(embeds=embed, files=file)

    @runnerreport.autocomplete("character_name")
    async def image_autocomplete(
        self, ctx: interactions.AutocompleteContext
    ) -> None:
        """Autocomplete for /runnerreport command."""

        character_name: str = ctx.input_text
        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.send(
                [
                    {
                        "name": str(self.report_db[i])
                        .replace("runner_report_", "")
                        .replace(".jpg", "")
                        .replace("_", " ")
                        .title(),
                        "value": str(self.report_db[i]),
                    }
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
                        {
                            "name": str(i)
                            .replace("runner_report_", "")
                            .replace(".jpg", "")
                            .replace("_", " ")
                            .title(),
                            "value": i,
                        }
                    )
            await ctx.send(choices)
