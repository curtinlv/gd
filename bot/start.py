from telethon import events

from .. import jdbot, chat_id, ch_name
from ..bot.utils import V4


@jdbot.on(events.NewMessage(from_users=chat_id, pattern='/start'))
async def bot_start(event):
    """接收/start命令后执行程序"""
    if V4:
        msg = '''使用方法如下：
    /help 获取命令，可直接发送至 @BotFather 。
    /start 开始使用本程序。
    /restart 重启本程序。
    e 查看运行日志。
    /up 升级本程序。
    /ver 查看程序版本号。
    /user 启动TG监控。
    /a 使用你的自定义快捷按钮。
    /addcron 增加crontab命令。
    /clearboard 删除快捷输入按钮。
    /blockcookie 屏蔽cookie操作。
    /checkcookie 检测cookie过期。
    /cmd 执行shell命令。
    /cron 进行cron管理。
    /edit 从目录选择文件并编辑，需要将编辑好信息全部发给BOT，BOT会根据你发的信息进行替换。建议仅编辑config或crontab.list，其他文件慎用！！！
    /getfile 获取/jd目录下文件。
    /log 查看脚本执行日志。
    /node 执行js脚本，输入/node xxxxx.js。建议使用snode命令。
    /set 设置。
    /setname 设置命令别名。
    /setshort 设置自定义按钮，每次设置会覆盖原设置。
    /snode 选择脚本执行，只能选择/scripts和/own目录下的脚本，选择完后直接后台运行。
    /repo 管理添加的仓库。
    /export 管理添加的环境变量。
    
    此外，直接发送文件至BOT，会让您选择保存到目标文件夹，支持保存并运行。发送以 .git 结尾的链接开始添加仓库。发送以 .js .sh .py结尾的已raw链接开始下载文件。发送格式为 key="value" 或者 key='value' 的消息开始添加环境变量。'''
    else:
        msg = '''使用方法如下：
    /help 获取命令，可直接发送至botfather。
    /start 开始使用本程序。
    /restart 重启本程序。
    e 查看运行日志。
    /up 升级本程序。
    /ver 查看程序版本号。
    /user 启动TG监控。
    /a 使用你的自定义快捷按钮。
    /addcron 增加crontab命令。
    /clearboard 删除快捷输入按钮。
    /blockcookie 屏蔽cookie操作。
    /checkcookie 检测cookie过期。
    /cmd 执行shell命令。
    /cron 进行cron管理。
    /edit 从目录选择文件并编辑，需要将编辑好信息全部发给BOT，BOT会根据你发的信息进行替换。
    /env 环境变量管理，仅支持青龙面板。
    /getfile 获取/ql目录下文件。
    /log 查看脚本执行日志。
    /node 执行js脚本，输入/node xxxxx.js。建议使用snode命令。
    /set 设置。
    /setname 设置命令别名。
    /setshort 设置自定义按钮，每次设置会覆盖原设置。
    /snode 选择脚本执行，只能选择/scripts和/own目录下的脚本，选择完后直接后台运行。
    /repo 管理添加的仓库。
    /addenv 青龙新增环境变量。
    /env 青龙管理环境变量。
    
    此外，直接发送文件至BOT，会让您选择保存到目标文件夹，支持保存并运行。发送以 .git 结尾的链接开始添加仓库。发送以 .js .sh .py结尾的已raw链接开始下载文件。发送格式为 key="value" 或者 key='value' 的消息开始添加环境变量。'''
    await jdbot.send_message(chat_id, msg)

if ch_name:
    jdbot.add_event_handler(bot_start,events.NewMessage(from_users=chat_id, pattern='开始'))
