
import os
from dotenv import load_dotenv
from pathlib import Path
import roboyml
from canvasgrades import CanvasGradeFile
import github.GithubException
from github import Github
from settings import *
import argparse


gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")

parser = argparse.ArgumentParser()
parser.add_argument('gradefile', type=str)
args = parser.parse_args()

commentors = set()

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for teamname, team in teams.items():
        gh_repo = utkcs.get_repo(teamname)
        gh_issues = gh_repo.get_issues()

        # print(f"Iterating issues for {teamname} ...")
        for issue in gh_issues:
            for comment in issue.get_comments():
                if (comment.created_at.date() == assignment_activity_estimates_due.date() 
                    or comment.updated_at.date() == assignment_activity_estimates_due.date()):
                    # print(f"Adding {comment.user.login} for comment made on {comment.created_at.date()}.")
                    commentors.add(comment.user.login)


with CanvasGradeFile(Path(args.gradefile)) as gradebook, roboyml.open(studentfile) as students: 
    for i, graderow in enumerate(gradebook.rows):
        if graderow[canvas_netid_col] not in students.keys():
            print(f"WARN: {graderow[canvas_netid_col]} not in students.yml")
            continue
        student = students[graderow[canvas_netid_col]]

        if student['github'] in commentors:
            # print(f"Found {graderow[canvas_netid_col]} in commentors.")
            graderow[assignment_activity_estimates] = 1
        else:
            graderow[assignment_activity_estimates] = 0
            
