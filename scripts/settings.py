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
ta_assignment_file = Path("ta-assignments.yml")

class_timezone = pytz.timezone('America/New_York')
a_week = timedelta(days=7)
iterations_due = {
    0: dt_parse("Thursday September 16th 23:59 2021"),
    1: dt_parse("Thursday October    7th 23:59 2021"),
    2: dt_parse("Thursday October   21st 23:59 2021"),
    3: dt_parse("Thursday November   4th 23:59 2021"),
}
iterations_due_aware = {
    n: d for n, d in ((n, class_timezone.localize(d)) for n, d in iterations_due.items())
}

canvas_netid_col = "SIS Login ID"
assignment_student_pr = "Individual PR (1061014)"
assignment_activity_estimates = "Activity - Estimates (1063234)"
assignment_activity_estimates_due = dt_parse("Thursday September 21st 23:59 2021 EST")
assignment_student_pr_due = dt_parse("Thursday September 9th 23:59 2021 EST")
assignment_team_pr = "Team PR (1061015)"
assignment_team_pr_due = dt_parse("Thursday September 16th 23:59 2021 EST")


if __name__ == "__main__":
    for n, d in iterations_due_aware.items():
        print(f"Iteration {n}: {d}")
