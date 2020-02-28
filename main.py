import traceback
import datetime
from wxpy import *
from config import logger
from app.utils import getDuration
from app.utils import getEnvVariable
from app.redmine_issues_hooker import getRedmine
from app.redmine_issues_hooker import getTargetIssues
from app.redmine_issues_hooker import blablaUpdateIssue
from app.redmine_issues_hooker import getRedmine
from app.wechat_hooker import initBot
from app.wechat_hooker import createWechatLogger
from app.wechat_hooker import getTargetGroup
from app.wechat_hooker import logOutBot
from app.wechat_hooker import talkToGroup

import sys

groupName = 'GROUP_NAME'

def testRedmine():
    try :
        envVar = getEnvVariable()
        redmine = getRedmine(envVar)
        targetIssues = getTargetIssues(redmine, envVar[targetProjectName], envVar[issueTimer], envVar[trackFreq])
        blablaUpdateIssue(targetIssues)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
#         log(2, "Oopus, error occurs! Error: " + str(e))
        logger.critical("Oopus, error occurs! Error: " + str(e))

def testWechat(bot):

    loggerWehat = createWechatLogger(bot)
    targetGroup= getTargetGroup(bot, loggerWehat)
    if targetGroup != None:
        msg = "Hi I am too hungry.."
        talkToGroup(targetGroup, msg, loggerWehat)
    else:
        logger.error("Can not locate target group.")
    bot.join()

if __name__== "__main__":
    # testRedmine()
    print("start bot test ...")
    bot = None
    # bot = initBot()
    try:
        bot = Bot(cache_path=True, console_qr=True)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.critical("Oopus, error occurs when log in wechat! Error: " + str(e))
    print("create bot...")
    testWechat(bot)
