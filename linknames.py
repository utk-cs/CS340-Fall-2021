
from pathlib import Path
import yaml
import re

students = {}
studentdir = Path("students")
studentoutput = Path("students.yml")

pattern = re.compile(r".*?:\W*(?P<name>[\w \-]+)\n+.*?:\W*(?P<netid>\w+)\W*\n+.*?:\W*(?P<github>[\w\-_]+)", re.M & re.I & re.S)

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
    students[netid] = {
        "netid": matches.group('netid'),
        "name": matches.group('name'),
        "github": matches.group('github'),
    }

with studentoutput.open('w') as outfile:
    yaml.dump(students, outfile)
