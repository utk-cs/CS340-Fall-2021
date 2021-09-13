import os
from pathlib import Path
from datetime import timedelta, datetime

from dotenv import load_dotenv
from dateutil.parser import parse as dt_parse

load_dotenv()

teamfile = Path("teams.yml")
studentfile = Path("students.yml")
repofile = Path("repos.yml")

iterations_due = {
    1: dt_parse("Thursday October  7th 23:59 2021"),
    2: dt_parse("Thursday October 21st 23:59 2021"),
    3: dt_parse("Thursday November 4th 23:59 2021"),
}
