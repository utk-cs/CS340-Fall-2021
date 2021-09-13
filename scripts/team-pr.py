
import os
from dotenv import load_dotenv
from pathlib import Path
import roboyml
import github.GithubException
from github import Github
from settings import *

gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")
ta_team = utkcs.get_team_by_slug("tas")
class_repo = utkcs.get_repo("CS340-Fall-2021")

team_label = class_repo.get_label("teams")
pulls = list(class_repo.get_pulls(state="all"))

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for netid, student in students.items():
        print(f">>> Processing {student['name']} ...")
        assigned_pulls = [p for p in pulls if student['github'] in [
            u.login for u in p.assignees
        ]]
        # print(f"{student['name']} is assigned to {assigned_pulls}")
        team_pulls = [p for p in assigned_pulls if team_label in p.labels and not (p.state == "closed" and p.merged == False)]
        if len(team_pulls) > 1:
            print(f"ERROR: {student['github']} is assigned to more than one team PR: {[p.number for p in team_pulls]}")
            students[netid]['team_pr'] = {
                "pr": [p.number for p in team_pulls],
                "state": "DUPLICATE",
                "merged": "Cannot merge, invalid team PR",
            }
        elif len(team_pulls) == 0:
            students[netid]['team_pr'] = None
        else:
            students[netid]['team_pr'] = {
                "pr": team_pulls[0].number,
                # "link": team_pulls[0].review_comments_url,
                "state": team_pulls[0].state,
                "merged": team_pulls[0].merged,
            }

    print(f"{len(students)} processed")
