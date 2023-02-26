"""
Root bot file.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import traceback
import interactions
from const import TOKEN, VERSION, EXTS

client = interactions.Client(
    intents=interactions.Intents.DEFAULT,
    activity=interactions.Activity(
        name=f"for SFSB v{VERSION}",
        type=interactions.ActivityType.WATCHING,
    ),
    send_command_tracebacks=False,
    show_ratelimit_tracebacks=True,
    basic_logging=True,
)
all_servers: list[int] = []
counted: bool = False

[client.load_extension(f"exts.{ext}") for ext in EXTS]


@client.listen()
async def on_startup() -> None:
    """Fires up STARTUP"""

    websocket = f"{client.latency * 1:.0f}"
    log_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).strftime("%d/%m/%Y %H:%M:%S")
    logging.debug(
        """[%s] Logged in as %s. Latency: %sms.""",
        log_time,
        client.user.username,
        websocket,
    )
    print(
        f"""[{log_time}] Logged in as {client.user.username}. Latency: {websocket}ms.\nIn {len(client.guilds)} guilds."""
    )


@client.listen()
async def on_command_error(ctx: interactions.events.CommandError) -> None:
    """For every Exception callback."""

    if not isinstance(ctx.ctx, interactions.SlashContext):
        return

    _ctx: interactions.SlashContext = ctx.ctx

    error_time = (
        datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    ).timestamp()

    error: Exception = ctx.error
    traceb2 = traceback.format_exception(
        type(error),
        value=error,
        tb=error.__traceback__,
        limit=1000,
    )
    traceb = "".join(traceb2)
    traceb = traceb.replace("`", "")
    traceb = traceb.replace("\\n", "\n")
    traceb = traceb.replace("\\t", "\t")
    traceb = traceb.replace("\\r", "\r")
    traceb = traceb.replace("\\", "/")
    er = ""
    for i in traceb:
        er = er + f"{i}"

    embed = interactions.Embed(
        title="**Uh oh...**",
        description="".join(
            [
                "An error occurred. The developer team is dealing with the ",
                " problem now.\nHave any question? ",
                "Join the [**support server**](https://discord.gg/ndy95mBfJs)",
                " for more help.",
            ]
        ),
        color=0xED4245,
        fields=[
            interactions.EmbedField(
                name="Error",
                value=f"```py\n{type(error).__name__}: {error}\n```",
            ),
        ],
    )

    await _ctx.send(embeds=embed, ephemeral=True)

    log_channel = client.get_channel(1065211632730513448)
    command_name: str = _ctx.command.name
    subcommand_name: str = None
    if _ctx.command.is_subcommand:
        subcommand_name = _ctx.command.to_dict().get("name")
    full_command = (
        f"""{command_name}{" " + subcommand_name if subcommand_name else ""}"""
    )

    log_error = interactions.Embed(
        title="An error occurred!",
        description="".join(
            [
                f"""Caused by **/{full_command}**\n""",
                f"Author: {_ctx.user.username}#{_ctx.user.discriminator} ``{_ctx.user.id}``\n",
                f"Guild: {_ctx.guild.name} ``{_ctx.guild.id}``\n",
                f"Occurred on: <t:{round(error_time)}:F>",
            ]
        ),
        color=0xED4245,
        fields=[
            interactions.EmbedField(
                name="Traceback",
                value=f"```\n{traceb}\n```"
                if len(traceb) < 1024
                else f"```\n...{traceb[-1000:]}\n```",
            )
        ],
    )

    await log_channel.send(embeds=log_error)


client.start(TOKEN)
