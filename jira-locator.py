import sys
import commands
from collections import defaultdict

def handleBranch(branchName, jiraIdFilename, map):
  # handle tags and
  for jira in open(jiraIdFilename):
    jira = jira.strip()
    cmd = 'git log | grep -i "' + jira + '" | wc -l'
    print "run .. " + cmd
    (sts, output) = commands.getstatusoutput(cmd)
    if sts != 0:
      pass

    if int(output) > 0:
      if not branchName.endswith('maint'):
        branchName = branchName[branchName.index('HDP'):]
        print "branchName after process:" + branchName
      map[jira].append(branchName)

if __name__ == "__main__":
  # args: <JIRA_ID_FILE_TO_CHECK>
  (sts, output) = commands.getstatusoutput('git branch -a | grep "HDP-2"')
  if sts != 0:
      raise Exception(output)

  map = defaultdict(list)
  jiraIdFilename = sys.argv[1]

  branches = output.split('\n')
  branches.append('2.2-maint')
  branches.append('2.3-maint')
  for b in branches:
    cmd = 'git checkout ' + b
    print cmd

    (sts, output) = commands.getstatusoutput('git checkout ' + b)
    if sts != 0:
      print "ERROR:" + output
      pass

    print "processing.. " + b
    handleBranch(b, jiraIdFilename, map)

  for jira in open(jiraIdFilename):
    jira = jira.strip()
    if map.__contains__(jira):
      print jira + ":" + str(map[jira])
    else:
      print jira + ' --- not included by any HDP branch ---'


