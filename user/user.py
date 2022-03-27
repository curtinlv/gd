#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from asyncio import sleep
import asyncio
import os
import re
import sys
from telethon import events
from .login import user
from .. import chat_id, jdbot, logger, TOKEN
from ..bot.utils import cmd, V4 
from ..diy.utils import rwcon, myzdjr_chatIds

bot_id = int(TOKEN.split(":")[0])
myzdjr_chatIds.append(bot_id)
client = user


@client.on(events.NewMessage(chats=bot_id, from_users=chat_id, pattern=r"^user(\?|\？)$"))
async def user(event):
    try:
        msg = await jdbot.send_message(chat_id, r'`靓仔你好，监控已正常启动！`')
        await asyncio.sleep(5)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=myzdjr_chatIds, pattern=r'export\s(computer_activityId|comm_activityIDList|jd_mhurlList|jd_nzmhurl|wish_appIdArrList|jd_redrain_half_url|jd_redrain_url|M_WX_COLLECT_CARD_URL|M_WX_ADD_CART_URL|M_WX_LUCK_DRAW_URL|jd_cjhy_activityId|jd_zdjr_activityId).*=(".*"|\'.*\')'))
async def activityID(event):
    try:
        text = event.message.text
        if "computer_activityId" in text:
            name = "电脑配件"
        elif "comm_activityIDList" in text:
            name = "jdjoy_open通用ID任务"
        elif "jd_mhurlList" in text:
            name = "盲盒任务抽京豆"
        elif "jd_nzmhurl" in text:
            name = "女装盲盒抽京豆"
        elif "wish_appIdArrList" in text:
            name = "许愿池抽奖机"
        elif "jd_redrain_url" in text:
            name = "整点京豆雨"
        elif "jd_redrain_half_url" in text:
            name = "半点京豆雨"
        elif "M_WX_COLLECT_CARD_URL" in text:
            name = "集卡任务"
        elif "M_WX_ADD_CART_URL" in text:
            name = "WX加购任务"
        elif "jd_cjhy_activityId" in text:
            name = "cj组队瓜分"
        elif "jd_zdjr_activityId" in text:
            name = "lz组队瓜分"
        elif "M_WX_LUCK_DRAW_URL" in text:
            name = "转盘抽奖"
        elif "WXGAME_ACT_ID" in text:
            name = "打豆豆"
        else:
            return
        msg = await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量！')
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:
            if "export " not in message:
                continue
            kv = message.replace("export ", "")
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
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
            if "computer_activityId" in event.message.text:
                await cmd('task /ql/scripts/jd_computer.js now')
            elif "comm_activityIDList" in event.message.text:
                await cmd('task /ql/scripts/jd_joyjd_open.js now')
            elif "jd_mhurlList" in event.message.text:
                await cmd('task /ql/scripts/jd_mhtask.js now')
            elif "jd_nzmhurl" in event.message.text:
                await cmd('task /ql/scripts/jd_nzmh.js now')
            elif "wish_appIdArrList" in event.message.text:
                await cmd('task /ql/scripts/jd_wish.js now')
            elif "M_WX_COLLECT_CARD_URL" in event.message.text:
                await cmd('task /ql/scripts/m_jd_wx_collectCard.js now')
            elif "M_WX_ADD_CART_URL" in event.message.text:
                await cmd('task m_jd_wx_addCart.js now')
            elif "M_WX_LUCK_DRAW_URL" in event.message.text:
                await cmd('task m_jd_wx_luckDraw.js now')
            elif "WXGAME_ACT_ID" in event.message.text:
                await cmd('task jd_dadoudou.js now')
            elif "jd_cjhy_activityId" in event.message.text:
                await cmd('task /ql/scripts/jd_cjzdgf.js now')
            elif "jd_zdjr_activityId" in event.message.text:
                await cmd('task /ql/scripts/jd_zdjr.js now')
            elif "jd_redrain_url" in event.message.text:
                msg = await jdbot.send_message(chat_id, r'`更换整点雨url完毕\n请定时任务0 0 * * * jtask jd_redrain now')
                await asyncio.sleep(1)
                await jdbot.delete_messages(chat_id, msg)
            elif "jd_redrain_half_url" in event.message.text:
                msg = await jdbot.send_message(chat_id, r'`更换半点雨url完毕\n请定时任务30 21,22 * * * jtask jd_redrain_half now')
                await asyncio.sleep(1)
                await jdbot.delete_messages(chat_id, msg)
            else:
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

