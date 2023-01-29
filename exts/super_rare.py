"""
/super_rare command.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import json
import interactions


def get_max(current_level: int, card: int) -> int:
    levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    cards = [
        30,
        6,
        8,
        12,
        20,
        40,
        60,
        80,
        100,
        130,
        160,
        200,
        240,
        280,
        330,
        400,
    ]
    rings = [
        0,
        400,
        2500,
        5000,
        9000,
        16000,
        24000,
        32000,
        50000,
        70000,
        85000,
        100000,
        130000,
        160000,
        200000,
        240000,
    ]
    exps = [
        0,
        40,
        80,
        120,
        160,
        200,
        280,
        360,
        440,
        520,
        600,
        680,
        800,
        960,
        1120,
        1280,
    ]

    i = levels.index(current_level)

    left_card = card
    level = current_level
    total_rings = 0
    total_exps = 0

    while left_card >= cards[i]:
        left_card -= cards[i]
        total_rings += rings[i]
        total_exps += exps[i]
        if level == 15:
            level = 16
            break
        else:
            level += 1
            i += 1

    return (
        level,
        left_card,
        f" / {cards[level]}" if level != 16 else "",
        total_rings,
        total_exps,
    )


def get_reached(current_level: int, card: int, aimed_level: int) -> int:

    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    cards = [0, 6, 8, 12, 20, 40, 60, 80, 100, 130, 160, 200, 240, 280, 330, 400, 0]
    rings = [
        0,
        400,
        2500,
        5000,
        9000,
        16000,
        24000,
        32000,
        50000,
        70000,
        85000,
        100000,
        130000,
        160000,
        200000,
        240000,
        0,
    ]
    exps = [
        0,
        40,
        80,
        120,
        160,
        200,
        280,
        360,
        440,
        520,
        600,
        680,
        800,
        960,
        1120,
        1280,
        0,
    ]

    level = current_level
    i = levels.index(current_level + 1 if current_level == 0 else current_level)
    aimed_level_index = int(levels.index(aimed_level)) + 1
    total_cards = 0 if level != 0 else 30
    total_exps = 0
    total_rings = 0

    if level != 1:
        for i in range(i + 1, aimed_level_index):
            total_cards += cards[i]
            total_rings += rings[i]
            total_exps += exps[i]
    else:
        for i in range(i, aimed_level_index):
            total_cards += cards[i]
            total_rings += rings[i]
            total_exps += exps[i]

    total_cards -= card

    return total_cards, total_rings, total_exps


def natural_rings(rings: int) -> str:
    """
    Returns the rings number in natural format.

    :param rings: The number of rings.
    :type rings: int
    :return: The number of rings in natural format.
    :rtype: str
    """

    magnitude = 0
    while abs(rings) >= 1000:
        magnitude += 1
        rings /= 1000.0
    # add more suffixes if you need them
    return "%.1f%s" % (rings, ["", "K", "M"][magnitude]) if rings != 0 else 0


class Super_Rare(interactions.Extension):
    """Extension for /super_rare commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.char_db: dict = json.loads(
            open("./db/character.json", "r", encoding="utf8").read()
        )

    @interactions.extension_command(
        name="super_rare",
        description="Calculate the level your Super Rare character can get.",
    )
    @interactions.option("The current level of your character.")
    @interactions.option("The current amount of card for that character.")
    @interactions.option("The level you are aimed for.")
    @interactions.option("The name of the character.", autocomplete=True)
    async def super_rare(
        self,
        ctx: interactions.CommandContext,
        current_level: int,
        card: int,
        aimed_level: int = 16,
        character_name: str = None,
    ) -> None:
        """Calculate the level your Super Rare character can get."""

        if current_level > 17 or aimed_level > 17:
            return await ctx.send("Invalid Level (maximum is 16).", ephemeral=True)

        elif current_level == 16:
            return await ctx.send(
                "Your character has already reached the maximum level.", ephemeral=True
            )

        elif current_level > aimed_level or current_level == aimed_level:
            return await ctx.send(
                "Your aimed level cannot higher than/equal to your current level.",
                ephemeral=True,
            )

        image = None
        if character_name:
            name_lower = character_name.lower()
            super_rare_char = []
            for char in self.char_db.keys():
                if self.char_db[char]["rarity"] == "Super Rare":
                    super_rare_char.append(char)

            if name_lower in super_rare_char:
                image = self.char_db[name_lower]["image"]

        a = get_max("Super Rare", current_level, card)
        b = get_reached("Super Rare", current_level, card, aimed_level)

        embed = interactions.Embed(
            title="Rarity: Super Rare",
            color=0x8A32FB,
        )
        embed.add_field(
            name=f"\u200b",
            value="".join(
                [
                    f"<:upgrade:1064630801469276170> : {current_level} -> {a[0]}\n",
                    "<:superrarecard:1064631338218573954> : "
                    + (
                        f"{a[1]}{a[2]}\n"
                        if str(a[2]) != ""
                        else "Maximum Level Reached\n"
                    ),
                    f"<:ring:1064628961931440198> : {natural_rings(a[3])}\n",
                    f"<:exp:1064630336610381855>: {a[4]}",
                ]
            ),
            inline=True,
        )
        if int(b[0]) > 0:
            embed.add_field(
                name=f"\u200b",
                value="".join(
                    [
                        f"<:upgrade:1064630801469276170> : {current_level} -> {aimed_level}\n",
                        f"<:superrarecard:1064631338218573954> : {b[0]}\n",
                        f"<:ring:1064628961931440198> : {natural_rings(b[1])}\n",
                        f"<:exp:1064630336610381855>: {b[2]}",
                    ]
                ),
                inline=True,
            )
        if image:
            embed.set_thumbnail(url=image)

        await ctx.send(embeds=embed)

    @interactions.extension_autocomplete(command="super_rare", name="character_name")
    async def super_rare_char(
        self, ctx: interactions.CommandContext, character_name: str = ""
    ) -> None:
        """Autocomplete for /super_rare command."""

        super_rare_char = {}
        for i in list(self.char_db.items()):
            if i[1]["rarity"] == "Super Rare":
                super_rare_char[i[0]] = i[1]

        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(name=super_rare_char[name]["name"], value=name)
                    for name in (
                        list(super_rare_char.keys())[0:9]
                        if len(super_rare_char) > 10
                        else list(super_rare_char.keys())
                    )
                ]
            )
        else:
            choices: list = []
            for char_name in super_rare_char:
                focus: str = "".join(letters)
                if focus.lower() in char_name.lower() and len(choices) < 20:
                    choices.append(
                        interactions.Choice(
                            name=super_rare_char[char_name]["name"], value=char_name
                        )
                    )
            await ctx.populate(choices)


def setup(client) -> None:
    """Setup the extension."""

    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Super_Rare(client)
    logging.debug("""[%s] Loaded Super Rare extension.""", log_time)
