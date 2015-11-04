import sys
import commands
from pygit2 import init_repository
from pyparsing import keepOriginalText


def matchStrings(str, patterns):
  str = str.lower()
  for p in patterns:
    if str.__contains__(p.lower()):
      return True
  return False

if __name__ == "__main__":
  # argv:
  # 1. all commits in the branch
  # 2. end commit
  whiteListCommits = set([])
  messageFilters = ["YARN-4032"]
  projectFilters = ["YARN-"]

  print sys.argv

  # get commits to look at
  allCommits = [line.strip() for line in open(sys.argv[1])]
  commitsToLookAt = []
  for commit in allCommits:
    if commit == sys.argv[2]:
      break
    commitsToLookAt.append(commit)

  # open repository
  repo = init_repository('/Users/wtan/sandbox/hadoop-common-trunk-test')

  keptCommits = []

  # look at commit to match
  for sha in commitsToLookAt:
    print "looking at commit=" + sha
    commit = repo.get(sha)
    commitMsg = unicode(commit.message).encode('ascii', 'ignore')

    print "DEBUG, commit.message:" + commitMsg

    keep = False
    if matchStrings(commitMsg, messageFilters):
      keep = True

    if whiteListCommits.__contains__(str(commit.id)):
      keep = True

    needLookAt = False
    if matchStrings(commitMsg, projectFilters):
      needLookAt = True
    else:
      keep = True

    if needLookAt and (not keep):
      # try to revert
      #(sts,output) = commands.getstatusoutput(
      #  'git revert --no-edit ' + sha + ' ||{ echo "ERROR_XXX"; export REVERT_FAILED=yes;' + ' git revert --abort; }')
      (sts,output) = commands.getstatusoutput(
        'git revert --no-edit ' + sha)
      if sts != 0:
        print "[Clean revert failed]: " + commitMsg + " Try to merge CHANGES.txt:"

        commands.getstatusoutput("git add hadoop-yarn-project/CHANGES.txt")
        (sts, output) = commands.getstatusoutput("git commit --no-edit")

        print "DEBUG: git commit --no-edit" + output

        if sts != 0:
          print "[CANNOT REVERT] commit=" + commitMsg + " skip.."
          commands.getstatusoutput("git revert --abort")
          keep = True
        else:
          print "[REVERTED]: " + commitMsg
      else:
        print "[REVERTED]: " + commitMsg

    if keep:
      keptCommits = [commit] + keptCommits

  # try to reapply all commits
  # 1. reset to first commit
  commands.getstatusoutput('git reset --hard ' + sys.argv[2])

  # showing all kept commits
  for commit in keptCommits:
    print "Will do cherry-pick:" + unicode(commit.message).encode('ascii', 'ignore')

  # 2. apply all commits
  for commit in keptCommits:
    commitMsg = unicode(commit.message).encode('ascii', 'ignore')
    (sts, output) = commands.getstatusoutput('git cherry-pick -x ' + str(commit.id) + ' --allow-empty')

    if sts != 0:
      print "DEBUG, failed to clean apply" + str(commit.id) + " msg=" + commitMsg
      print "Try to merge CHANGES.txt:"
      commands.getstatusoutput("git add hadoop-yarn-project/CHANGES.txt")
      (sts, output) = commands.getstatusoutput("git commit --no-edit --allow-empty")
      if sts != 0:
        print "output=" + output
        print "[FAILED TO CHERRY-PICK] " + " msg=" + commitMsg
        break
      else:
        print "[APPLIED] " + str(commit.id) + " msg=" + commitMsg
    else:
      print "[APPLIED] " + str(commit.id) + " msg=" + commitMsg

  # 3. print table:
  """
  ||Bug Type (bug/feature etc)||JIRA number||Internal SHA's of all commits (including reverts and reapplies)||External SHA1|| Owner||
  |feature|YARN-3365| | d8e17c58bcbff16c19bd2cba53a85baa7fec550b|[~sseethana]|
  |feature|YARN-3443| | 7c072bf0929352b9a0744853a909ae3c40560faf|[~sseethana]|
  |feature|YARN-3366| | 04783b04024c3396b156565a581b7461bcf7e031|[~sseethana]|
  """

  print "||Bug Type (bug/feature etc)||JIRA number||Internal SHA's of all commits (including reverts and reapplies)||External SHA1|| Owner||Description||"
  for commit in keptCommits:
    commitMsg = unicode(commit.message).encode('ascii', 'ignore')
    if matchStrings(commitMsg, projectFilters):
      print("||feature|" + commitMsg[commitMsg.find("YARN-"):commitMsg.find("YARN-")+9] + "| | " + str(commit.id) + "|[~wtan]|" + commitMsg[:min(30,len(commitMsg))] + "|")
