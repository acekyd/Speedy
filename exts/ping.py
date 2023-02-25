"""
/ping command.

(C) 2022-2023 - Jimmy-Blue
"""

import interactions


class Ping(interactions.Extension):
    """Extension for /ping command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="ping",
        description="Pong!",
    )
    async def ping(self, ctx: interactions.SlashContext) -> None:
        """Pong!"""

        websocket: int = int(f"{self.client.latency * 1000:.0f}")
        await ctx.send(f":ping_pong: Pong! **{websocket}ms**")
