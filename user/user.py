#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import random
import os
import re
import sys
import json
from telethon import events
from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import cmd, V4
from ..diy.utils import rwcon, myzdjr_chatIds, my_chat_id, jk
jk_version = 'v1.2.1'
from ..bot.update import version as jk_version

bot_id = int(TOKEN.split(":")[0])
# myzdjr_chatIds.append(bot_id)
client = user
## 新增配置自定义监控
jk_list = jk["jk"]
cmdName = jk["cmdName"]
jcDict = {}
dlDict = {}
try:
    isNow = jk["isNow"]
except Exception as e:
    isNow = True

nameList, envNameList, scriptPathList = [], [], []
for i in jk_list:
    if i["isOpen"]:
        nameList.append(i["name"])
        envNameList.append(i["envName"])
        scriptPathList.append(i["scriptPath"])
        dlDict[i["name"]] = 0
patternStr = ''
envNum = len(envNameList)
for i in range(envNum):
    if i == envNum-1:
        patternStr += envNameList[i] + "|jd_redrain_url|jd_redrain_half_url|zjdbody"
    else:
        patternStr += envNameList[i] + "|"

# 开启随机延时
if isNow:
    yanshi = ''
else:
    yanshi = 'now'

def readDL(lable, dl=dlDict):
    if lable:
        with open('duilie.json', "w+", encoding="utf-8") as f:
            json.dump(dl, f, ensure_ascii=False)
    else:
        with open('duilie.json', "r", encoding="utf-8") as f:
            dl = json.load(f)
    return dl


readDL(True)
########
# 开启队列
async def funCX(name, scriptPath, msg, lable=1):
    try:
        cxjc = f'ps -ef | egrep -v "timeout|grep" | grep {scriptPath} | egrep "python|node"'
        result = os.popen(cxjc)
        r = result.readlines()
        if r:
            a = random.randint(60, 180) #队列检测休眠时间
            msg = await jdbot.edit_message(msg, f"【队列】`[{name}]`当前已在跑，已加入队列等待。本次等待`{a}`秒后再次尝试。可发送【`监控明细`】查询队列情况。")
            if lable < 21:
                if lable == 1:
                    dl = readDL(False)
                    dl[name] += 1
                    readDL(True, dl)
                lable += 1
                await asyncio.sleep(a)
                return await funCX(name, scriptPath, msg, lable)
        else:
            msg = await jdbot.edit_message(msg, f"【队列】`[{name}]`当前空闲，后台将随机延时执行。")
    except Exception as e:
        print(e)
    return msg

# 查询当前已运行
async def funCXDL():
    dl = readDL(False)
    for n, i in zip(nameList, scriptPathList):
        cxjc = f'ps -ef | egrep -v "timeout|grep" | grep {i} | egrep "python|node"'
        result = os.popen(cxjc)
        r = result.readlines()
        jcDict[n] = len(r)
    dlmsg = ''
    for i in jcDict:
        if jcDict[i] > 0:
            jcNum = f'`{jcDict[i]}`'
        else:
            jcNum = jcDict[i]
        if dl[i] > 0:
            dlNum = f'`{dl[i]}`'
        else:
            dlNum = dl[i]
        dlmsg += f"当前:{jcNum} | 队列:{dlNum}\t【{i}】\n"
    if isNow:
        dlmsg += f"\n是否队列等待:`已开启`\n"
    else:
        dlmsg += f"\n是否队列等待:`未开启`（如需开启，请配置jk.json的参数isNow=true）\n"
    return dlmsg


@client.on(events.NewMessage(chats=bot_id, from_users=chat_id, pattern=r"^(user|在吗)(\?|\？)$"))
async def user(event):
    try:
        msg = await jdbot.send_message(chat_id, f'靓仔你好，gd监控`{jk_version}`已正常启动！\n\n配置变量: `{len(jk_list)}` | 当前监控: `{envNum}`')
        dlmsg = await funCXDL()
        await asyncio.sleep(3)
        msg = await jdbot.edit_message(msg, f'\n================\n\t\t\t\t\t\t\t监控明细\n================\n{dlmsg}')
        await asyncio.sleep(30)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")

@client.on(events.NewMessage(chats=bot_id, from_users=chat_id, pattern=r"^监控明细$"))
async def user(event):
    try:
        dlmsg = await funCXDL()
        await asyncio.sleep(3)
        msg = await jdbot.send_message(chat_id, f'\n================\n\t\t\t\t\t\t\t监控明细\n================\n{dlmsg}')
        await asyncio.sleep(30)
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
                scriptPath = '/ql/scripts/zxd.js'
                break
            elif "jd_redrain_url" in text:
                name = "整点京豆雨"
                scriptPath = 'xxxxxxxxx'
                break
            elif "jd_redrain_half_url" in text:
                name = "半点京豆雨"
                scriptPath = 'xxxxxxxxx'
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
                if isNow:
                    # name_p = f'{name}_{str(round(time.time() * 1000))}'
                    msg = await funCX(name, scriptPath, msg)
                    configs = rwcon("str")
                    if kv in configs:
                        continue
                # if 'VENDER_ID' in key:
                    # 防止同时触发开卡变量，自动加*` ？
                a = random.randint(3, 15)
                    # time.sleep(a)
                await asyncio.sleep(a)
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
                    dl = readDL(False)
                    if dl[name] > 0:
                        dl[name] -= 1
                        readDL(True, dl)
                    await cmd(f'{cmdName} {scriptPath} now')
                    # if isNow:
                    #     # await funCX(name, scriptPath)
                    #     await cmd(f'{cmdName} {scriptPath} {yanshi}')
                    # else:
                    #     await cmd(f'{cmdName} {scriptPath} now')
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
