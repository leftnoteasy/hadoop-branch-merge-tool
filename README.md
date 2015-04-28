# Overview
This tool is for backporting changes in trunk to branches

- You have a branch-x (for example branch-2.7), and a branch-y (e.g. branch-2.7. branch-x is forked from branch-y.
- There’re some commits cherry-picked from branch-2 to branch-2.7, and branch-2 has some new commits
- You wants to port a list of commits from branch-2 to branch-2.7, you need to know what’s the dependencies you need pull into branch-2.7

# Installation
- Install Pygit2 (http://www.pygit2.org/install.html)

# Usage (DO FOLLOWING ON A TEST REPOSITORY, AND DO NOT PUSH)
- Get all commits in branch-2 `git log | grep “^commit “ | awk ‘{print $2}’ > branch-2-commits`
- Get the first commit of branch-2.7: it’s 3c24e50ce2654a88c14d6897733435beab062212
- Edit main.py, add what you want
- Under the repository directory, switch to branch-2, run `python path/to/main.py branch-2-commits 3c24e50ce2654a88c14d6897733435beab062212 > output.log`
- This script will first try to revert all commits not wanted by you (but will ignore CHANGES.txt conflicts). And reset —hard to first commit of branch-2.7, then cherry-pick left commits.
- You can check commits will be reverted, reapplied, etc. in output.log.
