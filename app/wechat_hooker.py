from wxpy import *
import traceback
from app.utils import getEnvVariable
from config import logger

groupName = 'GROUP_NAME'
loggerSwitch = 'WECHAT_LOGGER'
loggerRec='WECHAT_LOGGER_RECIEVER'
loggerRecName='WECHAT_LOGGER_RECIEVER_NAME'


#  Unused.....
def createWechatLogger(bot):
    # Create loggerWechat reciever
    envVar = getEnvVariable()
    reciever = None
    loggerWechat = None
    try:
        if envVar[loggerSwitch] == 'ON':
            if envVar[loggerRec] == 'group':
                reciever = ensure_one(bot.groups().search(envVar[loggerRecName]))
                loggerWechat = get_wechat_logger(reciever)
                logger.info("Createed wechat logger: " + envVar[loggerRec] + " name: " + envVar[loggerRecName])
            elif envVar[loggerSwitch] == 'person':
                reciever = ensure_one(bot.friends().search(envVar[loggerRecName]))
                loggerWechat = get_wechat_logger(reciever)
                logger.info("Createed wechat logger: " + envVar[loggerRec] + " name: " + envVar[loggerRecName])
            else:
                logger.warning("Can not create logger reciever because wrong configuration!")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Wechat bot can not find group or person: " + envVar[loggerRecName] + ", Error: " + str(e))
    return loggerWechat


def getTargetGroup(bot, loggerWechat=None):
    targetGroup = None
    try:
        envVar = getEnvVariable()
        targetGroup = ensure_one(bot.groups().search(envVar[groupName]))
        logger.warning(" Found target group: " + envVar[groupName])
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Oopus, error occurs when searching the target group in wechat! Error: " + str(e))
        # if loggerWechat:
        #     loggerWehat.error("Oopus, wechat bot can not find target group : " + envVar[groupName] + "! Error: " + str(e))
    return targetGroup

def logOutBot(bot, loggerWehat=None):
    try:
        logger.warning("Log out wechat bot.")
        bot.logout()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Oopus, error occurs when log out wechat! Error: " + str(e))
        # if loggerWehat:
        #     loggerWechat.error("Oopus, error occurs when log out wechat bot! Error: " + str(e))

def talkToGroup(group, msg, loggerWechat=None):
    try:
        group.send(msg)
        logger.warning(" Send a msg to target group: " + msg)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Oopus, error occurs when talk to group! Error: " + str(e))

        # if loggerWechat:
        #     loggerWechat.warning("Oopus, error occurs when talk to group ! " + str(e))
