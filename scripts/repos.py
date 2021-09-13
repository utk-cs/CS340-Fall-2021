
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta, datetime
from dateutil.parser import parse as dt_parse

import roboyml
import github.GithubException
from github import Github
from settings import *

gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")
ta_team = utkcs.get_team_by_slug("tas")

for k, dt in iterations_due.items():
    print(f"Iteration {k} due at {dt}")

with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams:
    for teamname, team in teams.items():
        print(f">>> Processing {teamname} ...")
        try:
            gh_team = utkcs.get_team_by_slug(teamname.lower())
            if gh_team == ta_team:
                raise ValueError(f"haha you tried - TA team needs to be separately managed")
            print(f"GitHub team: {gh_team}")
        except github.GithubException as e:
            if e.status != 404:
                raise e
            gh_team = utkcs.create_team(
                teamname,
                privacy="secret",
            )
            print(f"Created team: {gh_team}")

        team_members = list(gh_team.get_members())
        desired_members = [gh.get_user(u["github"]) for u in team["members"].values()]
        for m in desired_members:
            if m not in team_members:
                print(f"Adding {m} to the team ...")
                gh_team.add_membership(m)
        print(f"Team members: {desired_members}")

        try:
            gh_repo = utkcs.get_repo(teamname)
        except github.GithubException as e:
            if e.status != 404:
                raise e
            print(f"Creating repository for team ...")
            gh_repo = utkcs.create_repo(
                teamname,
                private=True,
                auto_init=True,
                gitignore_template="Python",
            )
        print(f"Repo: {gh_repo}")

        ta_team.update_team_repository(gh_repo, "admin")
        gh_team.update_team_repository(gh_repo, "maintain")

        gh_milestones = list(gh_repo.get_milestones())

        for i, dt in iterations_due.items():
            gh_milestone_name = f"Iteration {i}"
            for m in gh_milestones:
                if m.title == gh_milestone_name:
                    iteration_milestone = m
                    break
            else:
                iteration_milestone = gh_repo.create_milestone(
                    gh_milestone_name,
                )
            # GH doesn't store hours, only date
            if (not iteration_milestone.due_on) or iteration_milestone.due_on.date() != dt.date():
                print(f"team {teamname} iteration {i} changing due date to {dt} from {iteration_milestone.due_on} ...")
                iteration_milestone.edit(
                    gh_milestone_name,
                    due_on=dt,
                )

    print(f"{len(teams)} teams processed")
