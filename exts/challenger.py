"""
/challenger command.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
import json
import interactions


def get_max(rarity: str, current_level: int, card: int) -> int:
    levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    if rarity == "Challenger":
        cards = [
            500,
            20,
            50,
            100,
            170,
            250,
            350,
            500,
            700,
            1000,
            1400,
            1900,
            2500,
            3200,
            4000,
            5000,
        ]
        rings = [
            0,
            500,
            2500,
            8000,
            16000,
            32000,
            50000,
            80000,
            120000,
            150000,
            180000,
            240000,
            300000,
            400000,
            550000,
            750000,
        ]
        exps = [
            0,
            50,
            100,
            150,
            200,
            250,
            350,
            450,
            550,
            650,
            750,
            900,
            1050,
            1200,
            1350,
            1600,
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


def get_reached(rarity: str, current_level: int, card: int, aimed_level: int) -> int:

    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    if rarity == "Challenger":
        cards = [
            0,
            20,
            50,
            100,
            170,
            250,
            350,
            500,
            700,
            1000,
            1400,
            1900,
            2500,
            3200,
            4000,
            5000,
            0,
        ]
        rings = [
            0,
            500,
            2500,
            8000,
            16000,
            32000,
            50000,
            80000,
            120000,
            150000,
            180000,
            240000,
            300000,
            400000,
            550000,
            750000,
            0,
        ]
        exps = [
            0,
            50,
            100,
            150,
            200,
            250,
            350,
            450,
            550,
            650,
            750,
            900,
            1050,
            1200,
            1350,
            1600,
            0,
        ]

    level = current_level
    i = levels.index(current_level + 1 if current_level == 0 else current_level)
    aimed_level_index = int(levels.index(aimed_level)) + 1
    total_cards = 0 if level != 0 else 500
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


def get_color(char_class: str) -> int:
    """
    Get the color hex based on the character class.

    :param class: The class of the player
    :type class: str
    :return: The color hex of the appropriate class.
    :rtype: int
    """

    if char_class == "Challenger":
        return 0xC92828


class Challenger(interactions.Extension):
    """Extension for /challenger commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
        self.char_db: dict = json.loads(
            open("./db/character.json", "r", encoding="utf8").read()
        )

    @interactions.extension_command(
        name="challenger",
        description="Calculate the level your Challenger character can get.",
    )
    @interactions.option("The current level of your character.")
    @interactions.option("The current amount of card for that character.")
    @interactions.option("The level you are aimed for.")
    @interactions.option("The name of the character.", autocomplete=True)
    async def challenger(
        self,
        ctx: interactions.CommandContext,
        current_level: int,
        card: int,
        aimed_level: int = 16,
        character_name: str = None,
    ):
        """Calculate the level your Challenger character can get."""

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
            challenger_char = []
            for char in self.char_db.keys():
                if self.char_db[char]["rarity"] == "Challenger":
                    challenger_char.append(char)

            if name_lower in challenger_char:
                image = self.char_db[name_lower]["image"]

        a = get_max("Challenger", current_level, card)
        b = get_reached("Challenger", current_level, card, aimed_level)

        embed = interactions.Embed(
            title="Rarity: Challenger",
            color=0xC92828,
        )
        embed.add_field(
            name=f"\u200b",
            value="".join(
                [
                    f"<:upgrade:1064630801469276170> : {current_level} -> {a[0]}\n",
                    "<:challenger:1064631495341391903> : "
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
                        f"<:challenger:1064631495341391903> : {b[0]}\n",
                        f"<:ring:1064628961931440198> : {natural_rings(b[1])}\n",
                        f"<:exp:1064630336610381855>: {b[2]}",
                    ]
                ),
                inline=True,
            )
        if image:
            embed.set_thumbnail(url=image)

        await ctx.send(embeds=embed)

    @interactions.extension_autocomplete(command="challenger", name="character_name")
    async def challenger_char(
        self, ctx: interactions.CommandContext, character_name: str = ""
    ) -> None:

        challenger_char = {}
        for i in list(self.char_db.items()):
            if i[1]["rarity"] == "Challenger":
                challenger_char[i[0]] = i[1]

        if character_name != "":
            letters: list = character_name
        else:
            letters = []

        if len(character_name) == 0:
            await ctx.populate(
                [
                    interactions.Choice(name=challenger_char[name]["name"], value=name)
                    for name in (
                        list(challenger_char.keys())[0:9]
                        if len(challenger_char) > 10
                        else list(challenger_char.keys())
                    )
                ]
            )
        else:
            choices: list = []
            for char_name in challenger_char:
                focus: str = "".join(letters)
                if focus.lower() in char_name.lower() and len(choices) < 20:
                    choices.append(
                        interactions.Choice(
                            name=challenger_char[char_name]["name"], value=char_name
                        )
                    )
            await ctx.populate(choices)


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Challenger(client)
    logging.debug("""[%s] Loaded Challenger extension.""", log_time)
