
import os
from dotenv import load_dotenv
from pathlib import Path
import roboyml
import github.GithubException
from github import Github
from settings import *

gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")
# class_repo = utkcs.get_repo("CS340-Fall-2021")
# org_members = list(utkcs.get_members())
# invited_users = list(utkcs.invitations())

# student_label = class_repo.get_label("students")
# pulls = list(class_repo.get_pulls(state="all"))

commentors = set()

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for teamname, team in teams.items():
        gh_repo = utkcs.get_repo(teamname)
        gh_issues = gh_repo.get_issues()

        print(f"Iterating issues for {teamname} ...")
        for issue in gh_issues:
            # commentors.add(issue.user.login)
            for comment in issue.get_comments():
                commentors.add(comment.user.login)

    print(f"{len(teams)} processed, {len(commentors)} people have at least one comment on an issue")

    for netid, student in students.items():
        if student['github'] in commentors:
            print(f"{student['name']}, {student['netid']}, {student['github']}, made a comment")
