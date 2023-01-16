"""
/about command.
(C) 2022 - Jimmy-Blue
"""

import logging
import datetime
from typing import Union
import interactions


# def get_reached(rarity: str, current_level: int, card: int, aimed_level: Union[int, None]) -> int:
#     match rarity:
#         case "Common":
#             cards = [0, 30, 50, 90, 140, 200, 300, 450, 650, 900, 1300, 1700, 2250, 2950, 3700, 4600]
#             rings = []
#         case "Rare":
#             cards = [0, 10, 20, 40, 70, 120, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
#             rings = []
#         case "Super Rare":
#             cards = [0, 6, 8, 12, 20, 40, 60, 80, 100, 130, 160, 200, 240, 280, 330, 400]
#             rings = []
#         case "Special":
#             cards = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 350, 400, 450, 500, 600]
#             rings = []
#         case "Challenger":
#             cards = [0, 20, 50, 100, 170, 250, 350, 600, 700, 1000, 1400, 1900, 2500, 3200, 4000, 5000]
#             rings = []

#     level_index = levels.index(current_level)

#     aimed_level_index = levels.index(aimed_level)

#     total_cards = cards[level_index + 1]

#     for i in range(level_index + 2, aimed_level_index + 1):
#         total_cards += cards[i]

#     total_cards -= card

#     return total_cards


class Level(interactions.Extension):
    """Extension for /level commands."""

    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="common",
        description="Calculate the level your Common character can get.",
    )
    @interactions.option("The current level of your character.")
    @interactions.option("The current amount of card for that character.")
    @interactions.option("The level you are aimed for.")
    @interactions.option("The name of the character.")
    async def common(
        self,
        ctx: interactions.CommandContext,
        current_level: int,
        card: int,
        aimed_level: int = 16,
        character: int = None
    ):
        """Calculate the level your Common character can get."""

        if current_level > 17 or aimed_level > 17:
            return await ctx.send("Invalid Level (maximum is 16).", ephemeral=True)

        elif current_level == 16:
            return await ctx.send("Your character has already reached the maximum level.", ephemeral=True)

        def get_max(rarity: str, current_level: int, card: int) -> int:
            match rarity:
                case "Common":
                    cards = [0, 30, 50, 90, 140, 200, 300, 450, 650, 900, 1300, 1700, 2250, 2950, 3700, 4600]
                    rings = [0, 100, 400, 900, 1600, 2500, 3600, 5000, 6000, 8600, 11300, 18500, 22000, 23300, 28000, 33300]
                    exps = [0, 10, 20, 30, 40, 50, 70, 90, 110, 130, 150, 170, 200, 240, 280, 320]
                case "Rare":
                    cards = [0, 10, 20, 40, 70, 120, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
                    rings = [0, 200, 900, 1800, 3700, 6000, 9000, 12700, 18700, 26200, 33700, 41200, 48700, 60000, 75000, 90000]
                    exps = [20, 40, 60, 80, 100, 140, 180, 220, 260, 300, 340, 400, 480, 560, 640]
                case "Super Rare":
                    cards = [0, 6, 8, 12, 20, 40, 60, 80, 100, 130, 160, 200, 240, 280, 330, 400]
                    rings = [0, 400, 2500, 5000, 9000, 16000, 24000, 32000, 50000, 70000, 85000, 100000, 130000, 160000, 200000, 240000]
                    exps = [0, 40, 80, 120, 160, 200, 280, 360, 440, 520, 600, 680, 800, 960, 1120, 1280]
                case "Special":
                    cards = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 350, 400, 450, 500, 600]
                    rings = [0, 1000, 5000, 15000, 30000, 60000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 600000, 800000, 1000000]
                    exps = [0, 40, 80, 120, 160, 200, 280, 360, 440, 520, 600, 680, 800, 960, 1120, 1280]
                case "Challenger":
                    cards = [0, 20, 50, 100, 170, 250, 350, 500, 700, 1000, 1400, 1900, 2500, 3200, 4000, 5000]
                    rings = [0, 500, 2500, 8000, 16000, 32000, 50000, 80000, 120000, 150000, 180000, 240000, 300000, 400000, 550000, 750000]
                    exps = [0, 50, 100, 150, 200, 250, 350, 450, 550, 650, 750, 900, 1050, 1200, 1350, 1600]

            levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

            level_index = levels.index(current_level)

            left_card = card
            level = current_level

            for i in range(level_index + 1, 16):
                if left_card - cards[i] < 0:
                    break
                else:
                    level += 1
                    left_card -= cards[i]

            return level, left_card

        cards = [0, 30, 50, 90, 140, 200, 300, 450, 650, 900, 1300, 1700, 2250, 2950, 3700, 4600]
        level = get_max("Common", current_level, card)[0]
        left_card = get_max("Common", current_level, card)[1]
        level += 1
        max_level = get_max("Common", current_level, card)[0]

        await ctx.send(f"{current_level} ➡ {max_level} | {left_card}/{cards[levels.index(level)]}")


def setup(client) -> None:
    """Setup the extension."""
    log_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime(
        "%d/%m/%Y %H:%M:%S"
    )
    Level(client)
    logging.debug("""[%s] Loaded Level extension.""", log_time)
