
from pathlib import Path
import roboyml
import re

# students = {}
studentdir = Path("students")
# studentoutput = Path("students.yml")

studentfile = Path("students.yml")

pattern = re.compile(r".*?:\W*(?P<name>[\w \-]+?)[\W\n]+.*?:\W*(?P<netid>\w+)\W*\n+.*?:\W*(?P<github>[\w\-_]+)", re.M & re.I & re.S)

with roboyml.open(studentfile) as students:
    for studentfile in studentdir.glob('*.md'):
        netid = str(studentfile).split('.')[0].split('/')[1]
        with studentfile.open('r') as f:
            matches = pattern.match(f.read())
        if not matches:
            raise ValueError(f"{studentfile} did not match: {matches}")
        else:
            print(f"{studentfile} matched: {matches}")
        if matches.group('netid') != netid:
            raise ValueError(f"{studentfile} netid mismatch")

        if not students[netid]:
            students[netid] = {
                "netid": matches.group('netid'),
            }
        students[netid]["name"] = matches.group('name')
        students[netid]["github"] = matches.group('github')
