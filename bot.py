"""
Root bot file.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import interactions
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

[client.load(f"exts.{ext}") for ext in EXTS]


@client.event
async def on_ready():
    """Fires up READY"""
    websocket = f"{client.latency * 1:.0f}"
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    logging.debug(
        """[%s] Logged in as %s. Latency: %sms.""", log_time, client.me.name, websocket
    )
    print(f"""[{log_time}] Logged in as {client.me.name}. Latency: {websocket}ms.""")


client.start()
