"""
/about command.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions


class About(interactions.Extension):
    """Extension for /about commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="about",
        description="Information about Speedy.",
    )
    async def _about(self, ctx: interactions.CommandContext) -> None:
        """Information about Speedy."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/SFSB-Bot",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Invite me",
                url="""https://discord.com/api/oauth2/authorize?client_id=947339220823994388&permissions=8&scope=bot%20applications.commands""",
            ),
        ]

        embed = interactions.Embed(
            title="About Speedy",
            description="".join(
                [
                    "The All-in-one Sonic Forces: Speed Battle Discord bot. Check your",
                    " current character level, how many rings are need, look up for ",
                    "character sprites, images, Speedy has you covered.",
                ]
            ),
            color=0xFC920C,
            footer=interactions.EmbedFooter(text="Maintained by Blue#2095"),
        )

        await ctx.send(embeds=embed, components=button)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    About(client)
    logging.debug("""[%s] Loaded About extension.""", log_time)
