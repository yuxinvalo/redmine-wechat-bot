from redminelib import Redmine
import datetime
import traceback
from app.utils import getDuration
from app.utils import getEnvVariable
# from config import logger

targetProjectName = 'TARGET_PROJECT_NAME'
redmineUrl = 'REDMINE_URL'
issueTimer = 'ISSUE_TIMER'
statusFilter = 'STATUS_FILTER'
redmineWatcher = 'REDMINE_WATCHER'
redmineWatcherPasswd = 'REDMINE_WATCHER_PASSWD'
accessMode = 'ACCESS_MODE'
redmineKey = 'REMINE_KEY'
groupName = 'GROUP_NAME'
delay = 'DELAY'


import logging
logging.config.fileConfig("logger.ini")
logger = logging.getLogger("redmine-wechat-watcher")

def getRedmine(envVar):
    if envVar[accessMode] == 'key':
        redmine = Redmine(envVar[redmineUrl], key = envVar[redmineKey])
    elif envVar[accessMode] == 'account':
        redmine = Redmine(envVar[redmineUrl], username=envVar[redmineWatcher], password=envVar[redmineWatcherPasswd])
    else :
        logger.error("Please check your configuration, unkown access mode!")

    return redmine

def getTargetProjectId(redmine, projectName):
    logger.info("Read projects...")
    projects = redmine.project
    targetProjectId = None
    for project in projects.all():
        if project.name == projectName:
            logger.info("find target project: " + projectName + " with project id : " + str(project.id))
            targetProjectId = project.id
            break
    return targetProjectId

def getTargetIssues(redmine, projectName, targetProjectId, issueCheckTimer, lastWatchTime, prioritySet, statuesSet):
    targetIssues = []
    # now = datetime.datetime.now()

    issues = redmine.issue.filter(project_id = targetProjectId, sort='category:desc')
    logger.info("find " + str(len(issues)) + " issues in project : " + projectName)

    prioritySets = prioritySet.split(",")
    statuesSets = statuesSet.split(",")

    # get issue time filter constraint
    logger.debug("filter=ISSUE_TIMER: " + str(issueCheckTimer)  + " LAST WATCH TIME: "  + str(lastWatchTime))

    try:
        if int(issueCheckTimer) == -1:
            for issue in issues:
                logger.debug("issue# " + str(issue.id) + " updated " + str(issue.updated_on) + "lwt:" + str(lastWatchTime) + "| prio: " + issue.priority.name + " | stat:" + issue.status.name )
                if issue.updated_on > lastWatchTime:
                    if prioritySets[0] == -1 or  issue.priority.name in prioritySets:
                        logger.debug("Issue#" + str(issue.id) + " priority corresponding..")
                        if statuesSets[0] == -1  or issue.status.name in statuesSets:
                            logger.debug("Issue#" + str(issue.id) + " status corresponding...")
                            targetIssues.append(issue)


        elif int(issueCheckTimer) > 0:
            for issue in issues:
                logger.debug("issue " + str(issue.id) + " was updated on " + str(issue.updated_on) + " and last watch time:" + str(lastWatchTime))
                if issue.updated_on > lastWatchTime and \
                issue.created_on > now - datetime.timedelta(days=int(issueCheckTimer)):
                    if issue.updated_on > lastWatchTime:
                        if prioritySets[0] == -1 or  issue.priority.name in prioritySets:
                            if statuesSets[0] == - 1 or  issue.status.name in statuesSets:
                                targetIssues.append(issue)


        else:
            logger.error("issue timer config error!")
    except Exception as e:
        logger.critical("Oops, got error when check updated issues:" + str(e))
    logger.info("find " + str(len(targetIssues)) + " updated issues " + str(targetIssues) +" in project : " + projectName)
    return targetIssues

def blablaUpdateIssue(issuesToInfo):
    paroleAll = []
    envVar = getEnvVariable()
    def getHumanReadDuration(duration):
        if duration < 60:
            return str(duration)[0:2] + " seconds ago"
        elif duration < 3600 and duration >= 60:
            return str(duration/60)[0:2] + " minutes ago"
        elif duration < 86400 and duration >= 3600:
            return str(duration/3600)[0:1] + " hours ago"

    def getAssignedUser(issueUser):
        if 'assigned_to' in dir(issueUser):
            return str(issueUser.assigned_to.name)
        else:
            return "anyone"

    def getSubject(issueSubj):
        if 'subject' in dir(issueSubj):
            return str(issueSubj.subject)
        else:
            return "unknow subject title"

    if len(issuesToInfo) < 1 or issuesToInfo == None:
        logger.warning("No updated issues found.")

    else:
        envVar = getEnvVariable()
        for issue in issuesToInfo:
            duration = getDuration(issue.updated_on, datetime.datetime.now()-datetime.timedelta(hours=int(envVar[delay])), 'seconds')
            durationHumanRead = getHumanReadDuration(duration)
            parole = "Issue: #" + str(issue.id) + " Subject: " + issue.subject +"  (" + getAssignedUser(issue) +") updated " + \
            durationHumanRead + ": " + envVar[redmineUrl] + "issues/" + str(issue.id)
            logger.info(parole)
            paroleAll.append(parole)
    return paroleAll
