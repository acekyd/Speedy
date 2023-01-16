# import openpyxl
# import json
# import time
# start_time = time.time()

# print("Loading Excel...")
# df = openpyxl.load_workbook("sfsb-db.xlsx")

# print(f"Finished loading .xlsx file. Took {time.time() - start_time}")


# df1 = df["Sheet1"]

# # with open("test.json", "w") as jr:
# #     for i in range(1, 50):
# #         for row in range(0, df1.max_row):
# #             for col in df1.iter_cols(1, df1.max_column):
# #                 s = col[row].value
# #                 if isinstance(s, str):
# #                     json.dump(s, jr)
# # for row in range(0, df1.max_row):
# #     for col in df1.iter_cols(1, df1.max_column):
# #         s = col[row].value
# #         print(s)
# all_rows = []

# for row in df1:
#     current_row = []
#     for cell in row:
#         current_row.append(cell.value)
#     all_rows.append(current_row)

# db = json.loads(open("test.json", "r").read())

# for i in range(0, len(all_rows)):
#     s = all_rows[i]
#     db[str(s[2])] = {
#         "description": str(s[3]),
#         "type": str(s[0]),
#     }

# with open("test.json", "w") as jr:
#     json.dump(db, jr)

# print(f"Finished! Took {time.time() - start_time}")

current_level = 3
card = 4000


def get_max(rarity: str, current_level: int, card: int) -> int:
    levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    match rarity:
        case "Common":
            cards = [90, 30, 50, 90, 140, 200, 300, 450, 650, 900, 1300, 1700, 2250, 2950, 3700, 4600]
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

    level_index = levels.index(current_level)

    left_card = card
    level = current_level

    while left_card >= cards[level_index]:
        left_card -= cards[level_index]
        if level == 15:
            level = 16
            break
        else:
            level += 1
            level_index += 1

    return level, left_card, cards[level]


a = get_max("Common", current_level, card)

print(f"{current_level} ➡ {a[0]}\n{a[1]}/{a[2]}")
