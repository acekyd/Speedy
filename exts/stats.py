"""
Stats command.
(C) 2022-2023 - Jimmy-Blue
"""

import logging
import datetime
import platform
import interactions
from interactions.ext import molter
from const import VERSION


class Stats(molter.MolterExtension):
    """Extension for /stats command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.uptime = f"<t:{round(datetime.datetime.utcnow().timestamp())}:R>"
        self.python = platform.python_version()
        self.system = str(platform.platform())

    @interactions.extension_command(
        name="stats",
        description="Shows the stats of Speedy.",
    )
    async def _stats(self, ctx: interactions.CommandContext):
        """Shows the stats of Speedy."""

        latency = f"{self.client.latency * 1:.0f}ms"
        guild_count = len(self.client.guilds)
        user_count = 0
        for guild in self.client.guilds:
            user_count += guild.member_count

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Speedy",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Top.gg",
                url="https://top.gg/bot/947339220823994388",
            ),
        ]

        fields = [
            interactions.EmbedField(name="Version", value=VERSION, inline=True),
            interactions.EmbedField(
                name="Guilds",
                value=guild_count,
                inline=True,
            ),
            interactions.EmbedField(name="Users", value=user_count, inline=True),
            interactions.EmbedField(name="Latency", value=latency, inline=True),
            interactions.EmbedField(
                name="Python",
                value=self.python,
                inline=True,
            ),
            interactions.EmbedField(
                name="Uptime",
                value=self.uptime,
                inline=True,
            ),
            interactions.EmbedField(
                name="System",
                value=self.system,
                inline=True,
            ),
        ]
        thumbnail = interactions.EmbedImageStruct(url=self.client.me.icon_url)
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar_url}",
        )
        embed = interactions.Embed(
            title="Speedy Stats",
            color=0x7CB7D3,
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=button)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Stats(client)
    logging.debug("""[%s] Loaded Stats extension.""", log_time)
