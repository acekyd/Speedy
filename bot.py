"""
Root bot file.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import traceback
import interactions
from interactions.ext import wait_for, files
from const import TOKEN, VERSION, EXTS

# logging.basicConfig(level=logging.DEBUG)

client = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.DEFAULT,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                type=interactions.PresenceActivityType.GAME, name=f"SFSB ver {VERSION}"
            )
        ],
        status=interactions.StatusType.ONLINE,
    ),
    # disable_sync=True,
)

wait_for.setup(client)
files.setup(client)
[client.load(f"exts.{ext}") for ext in EXTS]


@client.event
async def on_start():
    """Fires up READY"""
    websocket = f"{client.latency * 1:.0f}"
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    logging.debug(
        """[%s] Logged in as %s. Latency: %sms.""", log_time, client.me.name, websocket
    )
    print(
        f"""[{log_time}] Logged in as {client.me.name}. Latency: {websocket}ms.\nIn {len(client.guilds)} guilds."""
    )


@client.event
async def on_command_error(ctx: interactions.CommandContext, error: Exception):
    """For every Exception callback."""

    error_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).timestamp()

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

    command_name = ctx.data._json["name"]
    subcommand_name = ctx.data._json.get("options", None)
    if subcommand_name:
        subcommand_name = subcommand_name[0]
        if subcommand_name["type"] == 1:
            subcommand_name = subcommand_name["name"]
        else:
            subcommand_name = None

    log_error = interactions.Embed(
        title="An error occurred!",
        description="".join(
            [
                f"""Caused by **/{command_name}{" " + subcommand_name if subcommand_name else ""}**\n""",
                f"Author: {ctx.user.username}#{ctx.user.discriminator} ``{ctx.user.id}``\n",
                f"Guild: {ctx.guild.name} ``{ctx.guild_id}``\n",
                f"Occurred on: <t:{round(error_time)}:F>",
            ]
        ),
        color=0xED4245,
        fields=[
            interactions.EmbedField(
                name="Traceback",
                value=f"```py\n{traceb}\n```"
                if len(traceb) < 1024
                else f"```py\n...{traceb[-1000:]}\n```",
            )
        ],
    )
    await ctx.send(embeds=log_error)


client.start()
