import traceback
import datetime
import time
from wxpy import *

from config import logger
from app.utils import getDuration
from app.utils import getEnvVariable

from app.redmine_issues_hooker import getRedmine
from app.redmine_issues_hooker import getTargetIssues
from app.redmine_issues_hooker import getTargetProjectId
from app.redmine_issues_hooker import blablaUpdateIssue
from app.redmine_issues_hooker import getRedmine

from app.wechat_hooker import createWechatLogger
from app.wechat_hooker import getTargetGroup
from app.wechat_hooker import logOutBot
from app.wechat_hooker import talkToGroup

groupName = 'GROUP_NAME'
targetProjectName = 'TARGET_PROJECT_NAME'
trackFreq = 'TRACK_FREQ'
issueTimer = 'ISSUE_TIMER'


def testRedmine():
    paroleAll = []
    try :
        envVar = getEnvVariable()
        redmine = getRedmine(envVar)
        projectId = getTargetProjectId(redmine, envVar[targetProjectName])
        lastWatchTime = datetime.datetime.now() - datetime.timedelta(hours=2)
        targetIssues = getTargetIssues(redmine, envVar[targetProjectName], projectId, envVar[issueTimer], lastWatchTime)
        paroleAll = blablaUpdateIssue(targetIssues)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
#         log(2, "Oopus, error occurs! Error: " + str(e))
        logger.critical("Oopus, error occurs! Error: " + str(e))
    return paroleAll

def testWechat(bot):
    paroleAll = testRedmine()
    loggerWechat = createWechatLogger(bot)
    if loggerWechat:
        logger.info("Wechat logger created.")
        loggerWechat.info("Wechat logger created.")
    else:
        logger.warning("Can not create wechat logger.")
    targetGroup= getTargetGroup(bot, loggerWechat)
    if targetGroup != None and len(paroleAll) != 0:
        for parole in paroleAll:
        # msg = "Hi I am too hungry.."
            talkToGroup(targetGroup, parole, loggerWechat)
    else:
        logger.info("Can not locate target group or no update messege.")
    # bot.join()

def timerController(bot, lastWatchTime):
    # trigger = True

    # Get configurations
    envVar = getEnvVariable()

    # Instance redmine object
    redmine = getRedmine(envVar)
    logger.debug("Got redmine instance...")

    # Get target project id to filter issues
    projectId = getTargetProjectId(redmine, envVar[targetProjectName])
    if projectId == None:
        logger.error("Can not locate project: " + projectName +  ", please check confi project name at app/redmine-wechat-bot.ini.")
        raise Exception("Can not locate project: " + projectName +  ", please check confi project name at app/redmine-wechat-bot.ini.")
    logger.debug("Got target project id...")

    #Create wechat logger to send log to wechat object
    # loggerWechat = createWechatLogger(bot)
    # if loggerWechat:
    #     logger.info("Wechat logger is  created.")
    #     loggerWechat.info("Wechat logger is created.")
    # else:
    #     logger.warning("Can not create wechat logger.")

    # Find target wechat group,  if  it shows that no group found, maybe you should speak in group or change group name to activate group search
    targetGroup= getTargetGroup(bot, None)
    if targetGroup == None:
        raise Exception("Target wechat group" + envVar[groupName] + " no found.")
    logger.debug("Target wechat group found...")

    while bot.alive:
        logger.warning("Start scanning at " + str(datetime.datetime.now()) +"...last watch time is: " + str(lastWatchTime))
        paroleAll = []
        try :
            # Watch updated issues after last watch time
            targetIssues = getTargetIssues(redmine, envVar[targetProjectName], projectId, envVar[issueTimer], lastWatchTime)
            logger.debug("Found updated issues : " + str(len(targetIssues)))
            for issue  in targetIssues:
                logger.debug("issue " + str(issue.id) + " was updated on " + str(issue.updated_on) + " and last watch time:" + str(lastWatchTime))
            paroleAll = blablaUpdateIssue(targetIssues)
            logger.debug("Found " + str(len(paroleAll)) + " updated issues..")

            if len(paroleAll) > 0:
                for parole in paroleAll:
                    talkToGroup(targetGroup, parole, None)
            else:
                logger.warning("No updated messege after " + str(lastWatchTime))

            lastWatchTime = lastWatchTime + datetime.timedelta(seconds=int(envVar[trackFreq]))
            logger.debug("Reassign last watch time to " + str(lastWatchTime) + "...")
            time.sleep(int(envVar[trackFreq]))
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.critical("Oopus, error occurs! Error: " + str(e))
            raise Exception("Error occurs when sending message to group: " + envVar[groupName])

    logger.warning("Wechat bot died.....")


if __name__== "__main__":
    # testRedmine()
    logger.info("Init wechat bot ...")
    lastWatchTime = datetime.datetime.now() -  datetime.timedelta(hours=1, seconds=100)
    logger.info("Timer starts from " + str(lastWatchTime))
    bot = None

    try:
         bot = Bot(cache_path=True, console_qr=True)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.critical("Oopus, error occurs when log in wechat! Error: " + str(e))
    if bot:
        print("creation of bot done, start redmine-wechat bot controller...")
        timerController(bot, lastWatchTime)


    # testWechat(bot)
