"""
Ping command.

(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions


class Ping(interactions.Extension):
    """Extension for /ping command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="ping",
        description="Pong!",
    )
    async def _ping(self, ctx: interactions.CommandContext) -> None:
        """Ping Articuno."""

        websocket = int(f"{self.client.latency * 1:.0f}")
        await ctx.send(f":ping_pong: Pong! **{websocket}ms**")


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Ping(client)
    logging.debug("""[%s] Loaded Ping extension.""", log_time)
