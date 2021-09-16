import os
from pathlib import Path
from datetime import timedelta, datetime
import pytz

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

canvas_netid_col = "SIS Login ID"
assignment_student_pr = "Individual PR (1061014)"
assignment_student_pr_due = dt_parse("Thursday September 9th 23:59 2021 EST")
assignment_team_pr = "Team PR (1061015)"
assignment_team_pr_due = dt_parse("Thursday September 16th 23:59 2021 EST")
