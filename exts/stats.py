"""
/stats command.

(C) 2023 - Jimmy-Blue
"""

import datetime
import platform
import interactions
from const import VERSION


class Stats(interactions.Extension):
    """Extension for /stats command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.uptime: float = datetime.datetime.utcnow().timestamp()
        self.python: str = platform.python_version()
        self.system: str = str(platform.platform())

    @interactions.slash_command(
        name="stats",
        description="Shows the stats of Speedy.",
    )
    async def stats(self, ctx: interactions.SlashContext) -> None:
        """Shows the stats of Speedy."""

        latency = f"{self.client.latency * 1000:.0f}ms"
        guild_count: str = str(len(self.client.guilds))
        user_count: int = 0
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
            interactions.EmbedField(
                name="Version", value=VERSION, inline=True
            ),
            interactions.EmbedField(
                name="Guilds",
                value=guild_count,
                inline=True,
            ),
            interactions.EmbedField(
                name="Users", value=f"{user_count}", inline=True
            ),
            interactions.EmbedField(
                name="Latency", value=latency, inline=True
            ),
            interactions.EmbedField(
                name="Python",
                value=self.python,
                inline=True,
            ),
            interactions.EmbedField(
                name="Uptime",
                value=f"<t:{round(self.uptime)}:R>",
                inline=True,
            ),
            interactions.EmbedField(
                name="System",
                value=self.system,
                inline=True,
            ),
        ]
        thumbnail = interactions.EmbedAttachment(
            url=self.client.user.avatar.url
        )
        footer = interactions.EmbedFooter(
            text=f"Requested by {ctx.user.username}#{ctx.user.discriminator}",
            icon_url=f"{ctx.user.avatar.url}",
        )
        embed = interactions.Embed(
            title="Speedy Stats",
            color=0x7CB7D3,
            footer=footer,
            thumbnail=thumbnail,
            fields=fields,
        )

        await ctx.send(embeds=embed, components=button)
