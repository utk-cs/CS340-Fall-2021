
import os
from dotenv import load_dotenv
from pathlib import Path
import roboyml
import github.GithubException
from github import Github
from settings import *

gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")
class_repo = utkcs.get_repo("CS340-Fall-2021")
org_members = list(utkcs.get_members())
invited_users = list(utkcs.invitations())

student_label = class_repo.get_label("students")
pulls = list(class_repo.get_pulls(state="all"))

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for netid, student in students.items():
        print(f">>> Processing {student['name']} ...")
        created_pulls = [p for p in pulls if student['github'].lower() == p.user.login.lower()]
        # print(f"{student['name']} is assigned to {assigned_pulls}")
        student_pulls = [p for p in created_pulls if student_label in p.labels and not (p.state == "closed" and p.merged == False)]
        if len(student_pulls) > 1 and not all([p.merged for p in student_pulls]):
            print(f"ERROR: {student['github']} has more than one PR: {[p.number for p in student_pulls]}")
            students[netid]['student_pr'] = {
                "pr": [p.number for p in student_pulls],
                "state": "DUPLICATE",
                "merged": "Cannot merge, duplicate exists",
            }
        elif len(student_pulls) == 0:
            students[netid]['student_pr'] = None
        else:
            students[netid]['student_pr'] = {
                "pr": student_pulls[0].number,
                # "link": student_pulls[0].review_comments_url,
                "state": student_pulls[0].state,
                "merged": student_pulls[0].merged,
                "merged_at": student_pulls[0].merged_at,
            }
            student_pull = student_pulls[0]
            if student['github'] in [u.login for u in org_members]:
                students[netid]['membership'] = "accepted"
            elif student['github'] in [u.login for u in invited_users]:
                students[netid]['membership'] = "invited"
            else:
                students[netid]['membership'] = None

    print(f"{len(students)} processed")
    print(f"The following students are not yet in the org:")
    for s in [s for n, s in students.items() if ('membership' not in s) or s['membership'] != "accepted"]:
        print(f"{s['name']}: {s['netid']} / {s['github']}" + (" (invited)" if ('membership' in s) and s['membership'] == "invited" else ""))
