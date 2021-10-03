
from pathlib import Path
import roboyml
import re

# teamdir = Path("teams")
# teamfile = Path("teams.yml")
# studentfile = Path("students.yml")
from settings import *

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams, roboyml.open(ta_assignment_file) as ta_assignments:
    unassigned_teamnames = list(teams.keys())
    for ta, teamnames in ta_assignments.items():
        for teamname in teamnames:
            unassigned_teamnames.remove(teamname)
            if teamname not in teams.keys():
                print(f"{ta} not linked to {teamname}")
            teams[teamname]["ta"] = ta
        print(f"{ta} responsible for {len(teamnames)} teams")

    print(f"Unassigned teams: {unassigned_teamnames}")
