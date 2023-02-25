"""
/about command.

(C) 2022-2023 - Jimmy-Blue
"""

import interactions


class About(interactions.Extension):
    """Extension for /about commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="about",
        description="Information about Speedy.",
    )
    async def _about(self, ctx: interactions.InteractionContext) -> None:
        """Information about Speedy."""

        button = [
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="GitHub",
                url="https://github.com/Jimmy-Blue/Speedy",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Invite Me",
                url="""https://discord.com/api/oauth2/authorize?client_id=947339220823994388&permissions=8&scope=bot%20applications.commands""",
            ),
            interactions.Button(
                style=interactions.ButtonStyle.LINK,
                label="Support Server",
                url="https://discord.gg/MUfUZ6knBf",
            ),
        ]

        embed = interactions.Embed(
            title="About Speedy",
            description="".join(
                [
                    "The All-in-one Sonic Forces: Speed Battle Discord bot. Check your",
                    " current character level, how many rings are need, look up for ",
                    "images, sprites, Speedy has you covered.",
                ]
            ),
            color=0x8CA9F3,
            footer=interactions.EmbedFooter(text="Maintained by Blue#2095"),
        )

        await ctx.send(embeds=embed, components=button)
