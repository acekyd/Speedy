"""
/about command.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
from interactions.ext import molter


class About(molter.MolterExtension):
    """Extension for /about commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="about",
        description="Information about {placeholder_name}.",
    )
    async def _about(self, ctx: interactions.CommandContext):
        """Information about {placeholder}."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/SFSB-Bot",
            ),
        ]

        embed = interactions.Embed(
            title="About {placeholder_name}",
            description="{placeholder_description}",
            color=0xfc920c,
            footer=interactions.EmbedFooter(
                text=f"Maintained by Blue#2095"
            ),
        )

        await ctx.send(embeds=embed, components=button)

    @molter.prefixed_command()
    async def about(self, ctx: molter.MolterContext):
        """Information about {placeholder}."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/SFSB-Bot",
            ),
        ]

        embed = interactions.Embed(
            title="About {placeholder_name}",
            description="{placeholder_description}",
            color=0xfc920c,
            footer=interactions.EmbedFooter(
                text=f"Maintained by Blue#2095"
            ),
        )

        await ctx.send(embeds=embed, components=button)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    About(client)
    logging.debug("""[%s] Loaded About extension.""", log_time)