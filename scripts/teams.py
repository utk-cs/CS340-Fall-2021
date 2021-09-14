
from pathlib import Path
import roboyml
import re

teamdir = Path("teams")
teamfile = Path("teams.yml")
studentfile = Path("students.yml")

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for teammd in teamdir.glob('*.md'):
        teamname = str(teammd).split('.')[0].split('/')[1]
        with teammd.open('r') as f:
            teamdata = f.read()
        if teamname not in teams:
            teams[teamname] = {}
        teams[teamname]["name"] = teamname
        teams[teamname]["members"] = {}

        for netid in students.keys():
            _r = re.compile(r'\b%s\b' % netid, re.I)
            if _r.search(teamdata):
                teams[teamname]["members"][netid] = {
                    "netid": students[netid]["netid"],
                    "github": students[netid]["github"],
                    "name": students[netid]["name"],
                }
                if "team" in students[netid]:
                    if students[netid]["team"] != teamname:
                        print(f"WARNING: student changed teams: {students[netid]} to {teamname}")
                students[netid]["team"] = teamname

    print(f"{len(students)} student entries, {len(teams)} teams")
