"""
/eval command.

(C) 2022-2023 - Jimmy-Blue
"""

import io
import textwrap
import inspect
import contextlib
import traceback
import interactions
from interactions.ext.paginators import Paginator


class Eval(interactions.Extension):
    """Extension for /eval command."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="eval",
        description="Evaluates some code.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="code",
                description="Code to evaluate.",
                required=True,
            )
        ],
    )
    async def eval(
        self, ctx: interactions.InteractionContext, code: str
    ) -> None:
        """Evaluates some code."""

        if int(ctx.user.id) != 892080548342820925:
            return await ctx.send(
                "You must be the bot owner to use this command. Also, no."
            )

        await ctx.defer()

        env = {
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "user": ctx.user,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
            "interactions": interactions,
            "client": self.client,
            "self.client": self.client,
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        try:
            exec(to_compile, env)
        except Exception:
            return await ctx.send(f"```py\n{traceback.format_exc()}\n```")

        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if value and len(value) < 1001:
                await ctx.send(f"```py\n{value}\n```")

            elif value and len(value) > 0:
                paginator = Paginator.create_from_string(
                    self.client,
                    content=value,
                    page_size=2000,
                    timeout=60,
                )
                await paginator.send(ctx)

            else:
                await ctx.send("```py\nNone\n```", ephemeral=True)
