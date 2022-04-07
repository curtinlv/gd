from telethon import events, Button
from .login import user

from .. import jdbot
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
import asyncio
import re
@user.on(events.NewMessage(pattern=r'^cb', outgoing=True))
async def CCBeanInfo(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await user.send_message(event.chat_id,'请指定要查询的账号,格式: cb 1 或 cb ptpin')
        return    
        
    key="BOTCHECKCODE"
    kv=f'{key}="{text}"'
    change=""
    configs = read("str")    
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
            change += f"【替换】环境变量:`{kv}`\n"  
            write(configs)
        else:
            configs = read("str")
            configs += f'export {key}="{text}"\n'
            change += f"【新增】环境变量:`{kv}`\n"  
            write(configs)
                
    if change!="":
        notification = await user.send_message(event.chat_id, change+'开始查询账号'+text+'的资产，请稍后...')
    else:
        notification = await user.send_message(event.chat_id, '开始查询账号'+text+'的资产，请稍后...')
        
    cmdtext="task /ql/repo/ccwav_QLScript2/bot_jd_bean_change.js now"        
    p = await asyncio.create_subprocess_shell(
        cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    res_bytes, res_err = await p.communicate()
    res = res_bytes.decode('utf-8') 
    txt=res.split('\n')
    strReturn=""
    if res:
        for line in txt:                
            if "】" in line or "明细" in line:
                strReturn=strReturn+line+'\n'
                    
    if strReturn:
        await notification.delete()
        await user.send_message(event.chat_id, strReturn)
    else:
        await notification.delete()
        await user.send_message(event.chat_id,'查询失败!')