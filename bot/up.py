import os
import sys
from asyncio import exceptions

import requests
from telethon import events

from .update import version, botlog
from .. import chat_id, jdbot, logger, JD_DIR, BOT_SET


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot$'))
async def myupbot(event):
    msg = await jdbot.send_message(chat_id, "/upbot 监控机器人暂不支持原bot更新，会冲突。请使用 `/upgd` 更新")
    return
    try:
        url = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/shell/bot.sh"
        if '下载代理' in BOT_SET.keys() and str(BOT_SET['下载代理']).lower() != 'false' and 'github' in url:
            url = f'{str(BOT_SET["下载代理"])}/{url}'
        resp = requests.get(url).text
        if "#!/usr/bin/env bash" not in resp:
            await jdbot.edit_message(msg, "【正式版本】\n\n下载shell文件失败\n请稍后重试，或尝试关闭代理重启")
            return
        with open(f"{JD_DIR}/bot.sh", 'w+', encoding='utf-8') as f:
            f.write(resp)
        text = "【正式版本】\n\n更新过程中程序会重启，请耐心等待……\n为安全起见，关闭user监控，请使用 /user 手动开启！"
        await jdbot.edit_message(msg, text)
        os.system(f"bash {JD_DIR}/bot.sh")
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ver$', incoming=True))
async def bot_ver(event):
    await jdbot.send_message(chat_id, f'当前版本\n{version}\n{botlog}')
