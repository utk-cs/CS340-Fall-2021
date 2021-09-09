
from pathlib import Path
import roboyml
import re

teamdir = Path("teams")
teamfile = Path("teams.yml")
studentfile = Path("students.yml")

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    print(f"Loaded {len(students)} student entries")

    for teammd in teamdir.glob('*.md'):
        teamname = str(teammd).split('.')[0].split('/')[1]
        with teammd.open('r') as f:
            teamdata = f.read()
        if teamname not in teams:
            teams[teamname] = {}
        teams[teamname]["name"] = teamname
        teams[teamname]["members"] = {}

        for netid in students.keys():
            if netid in teamdata:
                teams[teamname]["members"][netid] = {
                    "netid": students[netid]["netid"],
                    "github": students[netid]["github"],
                    "name": students[netid]["name"],
                }
                students[netid]["team"] = teamname
