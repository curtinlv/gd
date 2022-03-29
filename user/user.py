#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os
import re
import sys
from telethon import events
from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import cmd, V4
from ..diy.utils import rwcon, myzdjr_chatIds, my_chat_id, jk

bot_id = int(TOKEN.split(":")[0])
# myzdjr_chatIds.append(bot_id)
client = user

## 新增配置自定义监控
jk_list = jk["jk"]
cmdName = jk["cmdName"]
nameList, envNameList, scriptPathList = [], [], []
for i in jk_list:
    if i["isOpen"]:
        nameList.append(i["name"])
        envNameList.append(i["envName"])
        scriptPathList.append(i["scriptPath"])
patternStr = ''
envNum = len(envNameList)
for i in range(envNum):
    if i == envNum-1:
        patternStr += envNameList[i] + "|jd_redrain_url|jd_redrain_half_url|zjdbody"
    else:
        patternStr += envNameList[i] + "|"
########

@client.on(events.NewMessage(chats=bot_id, from_users=chat_id, pattern=r"^user(\?|\？)$"))
async def user(event):
    try:
        msg = await jdbot.send_message(chat_id, f'靓仔你好，监控已正常启动！\n\n配置变量: `{len(jk_list)}` | 当前监控: `{envNum}`')
        await asyncio.sleep(5)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=myzdjr_chatIds, pattern=r'export\s(%s).*=(".*"|\'.*\')' % patternStr))
async def activityID(event):
    try:
        text = event.message.text
        name = None
        for i in envNameList:
            if i in text:
                name = nameList[envNameList.index(i)]
                scriptPath = scriptPathList[envNameList.index(i)]
                break
            elif "zjdbody" in text:
                name = "赚喜豆-每天90豆"
                break
            elif "jd_redrain_url" in text:
                name = "整点京豆雨"
                break
            elif "jd_redrain_half_url" in text:
                name = "半点京豆雨"
                break
        if not name:
            return
        msg = await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量！')
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:
            if "export " not in message:
                continue
            kv = message.replace("export ", "")
            key = kv.split("=")[0]
            value = re.findall(r'[\'|"]([^"]*)[\'|"]', kv)[0]
            configs = rwcon("str")
            if kv in configs:
                continue
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            else:
                if V4:
                    end_line = 0
                    configs = rwcon("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            end_line = configs.index(config) - 1
                            break
                    configs.insert(end_line, f'export {key}="{value}"\n')
                else:
                    configs = rwcon("str")
                    configs += f'export {key}="{value}"\n'
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, f"【取消】 `{name}` 环境变量无需改动！")
            return
        try:
            lable = None
            for i in envNameList:
                if i in text:
                    lable = True
                    await cmd(f'{cmdName} {scriptPath} now')
                    break
                # 赚京豆助力，将获取到的团body发给自己测试频道，仅自己内部助力使用
                elif "zjdbody" in text:
                    lable = True
                    if str(event.message.peer_id.channel_id) in str(my_chat_id):
                        await cmd('task /ql/scripts/zxd.js now')
                    break
                elif "jd_redrain_url" in text:
                    lable = True
                    msg = await jdbot.send_message(chat_id, r'`更换整点雨url完毕\n请定时任务0 0 * * * task jd_redrain now')
                    await asyncio.sleep(1)
                    await jdbot.delete_messages(chat_id, msg)
                    break
                elif "jd_redrain_half_url" in text:
                    lable = True
                    msg = await jdbot.send_message(chat_id, r'`更换半点雨url完毕\n请定时任务30 21,22 * * * task jd_redrain_half now')
                    await asyncio.sleep(1)
                    await jdbot.delete_messages(chat_id, msg)
                    break
            if not lable:
                await jdbot.edit_message(msg, f"看到这行字,是有严重BUG!")
        except ImportError:
            pass
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
