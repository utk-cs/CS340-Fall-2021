
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta, datetime
from dateutil.parser import parse as dt_parse
import argparse

import roboyml
import github.GithubException
from github import Github
from settings import *

# gh = Github(os.environ.get("GITHUB_TOKEN"))

# utkcs = gh.get_organization("utk-cs")
# ta_team = utkcs.get_team_by_slug("taem")
ta_team = "taem"

# for k, dt in iterations_due.items():
#     print(f"Iteration {k} due at {dt}")

parser = argparse.ArgumentParser(description="Checker for student commits")

parser.add_argument(
    '--iteration', '-i',
    required=True,
    type=int,
    help="Iteration number",
)
parser.add_argument(
    '--ta', '-t',
    required=False,
    type=str,
    help="Only output for a certain TA's teams",
)
parser.add_argument(
    'file',
    type=Path,
    help="path to iteration commits file",
)


args = parser.parse_args()

gh_milestone_name = f"Iteration {args.iteration}"
iteration_timedelta = iterations_due[args.iteration] - iterations_due[args.iteration-1]
iteration_weeks = {
    x+1: 0 for x in range(round(iteration_timedelta / a_week))
}
for week_num in list(iteration_weeks.keys()):
    since = iterations_due[args.iteration-1] + (a_week * (week_num-1))
    until = iterations_due[args.iteration-1] + (a_week * (week_num))
    if since > datetime.now():
        print(f"Skipping week {week_num} which is in the future: {since}")
        del iteration_weeks[week_num]
    else:
        print(f"Iteration {args.iteration} Week {week_num} goes from {since} to {until}")

print(f"Checking weeks {list(iteration_weeks.keys())}")
print(f"INPUT: {args.file}")


with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams, roboyml.open(args.file) as commits, roboyml.open(ta_assignment_file) as ta_assignments:
    missed_a_week_of_commits = set()
    no_commits_in_week = {
        n: set() for n in iteration_weeks.keys()
    }
    for teamname, team in teams.items():
        if teamname == ta_team:
            continue
        if args.ta and teamname not in ta_assignments[args.ta]:
            continue

        # part 1: invalid commits
        invalid_commits = {
            sha: data for sha, data in commits[teamname]["bad_committer"].items()
        }
        for sha, c in invalid_commits.items():
            print(f"Invalid commit: {sha}: {c['html_url']}")

        for gh_username in (m["github"] for m in team["members"].values()):
            cdata = commits[teamname][gh_username]
            # if "weekly_count" not in cdata:
            #     print(f"{gh_username} has no count for their commits")
            for wn, count in cdata["weekly_count"].items():
                if wn not in no_commits_in_week:
                    continue
                if count == 0:
                    no_commits_in_week[wn].add(gh_username)

        print(f">>> Processing {teamname} ...")

    for n, users in no_commits_in_week.items():
        print(f"=== Week {n} zero commits ({len(users)}): {users}")
        missed_a_week_of_commits |= users

    print(f"Users who missed a week of commits: {len(missed_a_week_of_commits)}")

    emails = set()
    for gh_username in missed_a_week_of_commits:
        student = [s for s in students.values() if s['github'].lower() == gh_username.lower()]
        assert len(student) == 1
        student = student[0]
        emails.add(f"{student['netid']}@vols.utk.edu")

    print(f"Email list: {', '.join(emails)}")
