#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from telethon import events, Button
from ..bot.utils import press_event, V4
from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..user.user import jk_version


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upgd$'))
async def upgdjk(event):
    try:
        SENDER = event.sender_id
        btns = [Button.inline("Yes, I do.", data='yes'), Button.inline("No~", data='cancel')]
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            msg = await conv.send_message(f"您是否更新要curtinlv/gd库的监控", buttons=btns)
            convdata = await conv.wait_event(press_event(SENDER))
            res = bytes.decode(convdata.data)
            if res == 'cancel':
                await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                await jdbot.delete_messages(chat_id, msg)
                conv.cancel()
                return
            else:
                msg = await jdbot.edit_message(msg, f"好的，请稍等...\n`conf`目录配置文件如有变动，请自行更新到/ql/config\n\n自动升级可能存在风险，升级成功后会自动重启机器人。如有问题请到群讨论https://t.me/topstyle996")
                if jk_version == 'v1.1':
                    pass
            conv.cancel()
        if V4:
            await jdbot.send_message(chat_id, "抱歉！暂不支持v4在线更新监控！")
        else:
            os.popen('pm2 stop jbot')
            os.popen("ps -ef | grep jbot | grep -v grep | awk '{print $1}' |xargs kill -9")
            os.popen('rm -rf /ql/repo/gd')
            os.popen('cd /ql/repo/ && git clone https://git.metauniverse-cn.com/https://github.com/curtinlv/gd.git')
            os.popen('rm -rf /ql/jbot/*')
            os.popen('cp -a /ql/repo/gd/* /ql/jbot/')
            os.popen('pm2 start jbot')
            os.popen('rm -rf /ql/repo/dockerbot')
            os.popen('mkdir /ql/repo/dockerbot')
            os.popen('ln -sf /ql/repo/gd /ql/repo/dockerbot/jbot')

        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(upgdjk, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

