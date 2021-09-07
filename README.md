# CS340 Fall 2021

Welcome, this is the repo used to link your GitHub for your class work.

## Instructions

- Fork this repo to your account (under whichever GitHub account you'll be authoring commits from for this class)
- Clone your fork to your machine where you have your development environment installed
- Add a file under `students/` where the filename is `<your-netid>.md` and matches the example format. (Must at least include netid and GitHub username)
- Commit & push this change to your fork
- Open a PR to merge your fork's changes into this repo

Once your PR is open, we'll give feedback / review it if anything is wrong, otherwise it'll be merged and you're good to go!

After your team has a project repo created, feel free to delete your fork of this repo.

### If your PR has been merged

Once your student PR gets merged you should see an invite to join the utk-cs organization. This is where we'll be creating your team repos, so you'll need access to work on your projects.

## Teams

If you already know who you want to work with, you can follow this same process to create a file under `teams/`.

Name this file with a proposed name for your team. It should be a markdown file again, and your file and PR should include both GitHub usernames and NetIDs for each team member. If all your team members have already had their personal PR merged and you've all been added to the organization you should assign your other team members as reviewers. Once the whole team approves the PR and meets the project requirements, we'll merge your team's PR and create a repo for your team.

Team size: 3-5 (if you don't have your own team, you'll be matched into groups of mostly 4 per team after Thursday)

### Project requirements

We provide 3 projects or you're allowed to propose your own project, we ask that you stick with Python + Qt so that we are able to most effectively grade your work. If you don't have something in mind we will provide project ideas, and if you have something that's more than Python + Qt (using a database, other language, or something external) you'll have to get it approved by Dr. Henley first. (All the TAs need to be able to run/grade/evaluate your code and app.)

In addition to using Python and Qt you should use some other freely available / open API. Some examples include weather APIs, Wikipedia / free wikis, public APIs like GitHub's, etc. We're pretty generic about the term "API" so this could also include non-internet APIs like other python libraries, local services, or other non-gui frameworks. In general we're looking for you to demonstrate that you can create a UI that can interface with something else non-graphical.

If you aren't sure about a project idea, go ahead and open a PR for your team and we'll give you feedback there.

The 3 project options (if you do not wish to propose your own):

- A weather app that accesses an online, public (no or free authentication) API to retrieve weather data and display it graphically to the user, with some amount of interactivity
- A wiki reader that pulls data from an online wiki (e.g. Wikipedia), using the MediaWiki API and allowing users to do more than just read a page
- A note taking app that saves notes to a local file database (e.g. SQLite), lets users search their notes and export them, and has revision history or undo/redo functions
