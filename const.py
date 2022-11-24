"""
Constant file.

(C) 2022 - Jimmy-Blue
"""

import os
from dotenv import load_dotenv

load_dotenv()

global TOKEN
global VERSION
global EXTS

TOKEN = os.getenv("TOKEN")
VERSION = "4.11.0"
EXTS = [
    file.replace(".py", "")
    for file in os.listdir("exts")
    if not file.startswith("_")
]