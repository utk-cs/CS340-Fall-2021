
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

gh = Github(os.environ.get("GITHUB_TOKEN"))

utkcs = gh.get_organization("utk-cs")
ta_team = utkcs.get_team_by_slug("taem")

# for k, dt in iterations_due.items():
#     print(f"Iteration {k} due at {dt}")

parser = argparse.ArgumentParser(description="Checker for student commits")

parser.add_argument(
    '--iteration', '-i',
    required=True,
    type=int,
    help="Iteration number",
)

args = parser.parse_args()

gh_milestone_name = f"Iteration {args.iteration}"
iteration_timedelta = iterations_due[args.iteration] - iterations_due[args.iteration-1]
iteration_weeks = {
    x+1: 0 for x in range(round(iteration_timedelta / a_week))
}
for week_num in iteration_weeks.keys():
    since = iterations_due[args.iteration-1] + (a_week * (week_num-1))
    until = iterations_due[args.iteration-1] + (a_week * (week_num))
    print(f"Iteration {args.iteration} Week {week_num} goes from {since} to {until}")
iteration_output_file = Path(f"iteration_{args.iteration}_{datetime.now().strftime('%Y-%m-%d_%T')}.yml")
print(f"OUTPUT: {iteration_output_file}")


with roboyml.open(studentfile) as students, roboyml.open(teamfile) as teams, roboyml.open(iteration_output_file) as output, roboyml.open(ta_assignment_file) as ta_assignments:
    for teamname, team in teams.items():
        print(f">>> Processing {teamname} ...")
        gh_team = utkcs.get_team_by_slug(teamname.lower())
        if gh_team == ta_team:
            continue
        # team_members = list(gh_team.get_members())
        gh_repo = utkcs.get_repo(teamname)
        # print(f"GitHub team: {gh_team}")
        # print(f"GitHub repo: {gh_repo}")
        team_members = [gh.get_user(u["github"]) for u in team["members"].values()]
        # print(f"Members: {list(x.login for x in team_members)}")
        gh_milestones = list(gh_repo.get_milestones())

        gh_milestone = [m for m in gh_milestones if m.title == gh_milestone_name]

        output[teamname] = {
            x: {
                "weekly_count": iteration_weeks.copy(),
                "commits": {},
            } for x in (u.login for u in team_members)
        }
        output[teamname]["bad_committer"] = {}

        for week_num in iteration_weeks.keys():
            # now we iterate commits during this iteration:
            repo_commits = gh_repo.get_commits(
                since=iterations_due[args.iteration-1] + (a_week * (week_num-1)),
                until=iterations_due[args.iteration-1] + (a_week * (week_num)),
            )
            for commit in repo_commits:
                if not commit.author:
                    print(f"ERROR: Commit has no GitHub account: {commit.sha}")
                    output[teamname]["bad_committer"][commit.sha] = {
                        "user": None,
                        "week": week_num,
                        "html_url": commit.html_url,
                    }
                    continue
                if commit.author.login not in output[teamname]:
                    if commit.author.login in ta_assignments.keys():
                        # ignore commits from TAs
                        continue
                    print(f"ERROR: GitHub account not in team: {commit.author.login}")
                    output[teamname]["bad_committer"][commit.sha] = {
                        "user": commit.author.login,
                        "html_url": commit.html_url,
                        "week": week_num,
                    }
                    continue
                output[teamname][commit.author.login]["commits"][commit.sha] = {
                    "additions": commit.stats.additions,
                    "deletions": commit.stats.deletions,
                    "total": commit.stats.total,
                    "html_url": commit.html_url,
                    "week": week_num,
                }
                output[teamname][commit.author.login]["weekly_count"][week_num] += 1

    print(f"{len(teams)} teams processed")
