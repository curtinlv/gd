"""
要求：
    1、需要具备一定的 python3 知识；
    2、清楚自己需要编辑代码的区域；
    3、清楚自己需要导入的变量的位置和变量名。
"""

from .. import chat_id, jdbot, logger, API_ID, API_HASH, PROXY_START, proxy, CONFIG_DIR, SCRIPTS_DIR, OWN_DIR, BOT_DIR, \
    _DiyScripts, LOG_DIR, SHORTCUT_FILE, BOT_LOG_FILE, BOT_JSON_FILE, QR_IMG_FILE, BOT_SET_JSON_FILE_USER, \
    BOT_SET_JSON_FILE, ch_name, TOKEN, START_CMD, PROXY_TYPE, connectionType
from ..bot.utils import row, CRON_FILE, BEAN_LOG_DIR, CONFIG_SH_FILE, V4, QL, DIY_DIR, TASK_CMD, get_cks, split_list, \
    backup_file, press_event, cmd, get_ch_names, log_btn, snode_btn, mycron, mycron, add_cron_V4, add_cron, \
    cron_manage_QL, cron_manage_V4, cron_manage, env_manage_QL
from telethon import events, Button
from asyncio import exceptions

"""
如果需要导入 diy 目录内某个文件的变量或函数
from ..diy.xxx import xxx
例如：from ..diy.utils import ql_token
"""

"""
如果需要导入 bot 目录内某个文件的变量或函数
from ..bot.xxx import xxx
例如：from ..bot.utils import myck
"""

"""
如果需要导入其他第三方库
import xxx
例如：import json
"""


async def start():
    try:
        """
        try 部分则自由发挥即可
        """
        # 例如下行代码代表在调用且运行此函数时，机器人给你发送一条消息
        # await jdbot.send_message(chat_id, "Hello World") # （注释此行即可）
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def end():
    try:
        """
        try 部分则自由发挥即可
        """
        # 例如下行代码代表在调用且运行此函数时，机器人给你发送一条消息
        # await jdbot.send_message(chat_id, "Hello World") # （注释此行即可）
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def smiek_jd_zdjr():
    try:
        """
        try 部分则自由发挥即可
        """
        # 例如下行代码代表在调用且运行此函数时，机器人给你发送一条消息
        # await jdbot.send_message(chat_id, "Hello World") # （注释此行即可）
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def jd_joinTeam_activityId():
    try:
        """
        try 部分则自由发挥即可
        """
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def getcookie(jd_cookie):
    try:
        """
        try 部分则自由发挥即可
        jd_cookie 是传入的 cookie 具体值
        """
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def signCollectGift():
    try:
        """
        try 部分则自由发挥即可
        """
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def rush_lzclient():
    try:
        """
        try 部分则自由发挥即可
        """
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def gua_addCart():
    try:
        """
        try 部分则自由发挥即可
        """
    
    
    
    
    
    
    
    
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))
