from telethon import events, Button
# from .login import user

from .. import jdbot, user
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
import asyncio
import re

@user.on(events.NewMessage(pattern=r'^setbd', outgoing=True))
async def SetBeanDetailInfo(event):
    try:
        msg_text= event.raw_text.split(' ')
        if len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
            
        if text==None:
            await event.edit('请输入正确的格式: setbd 屏蔽京豆数量')
            return    
            
        key="BOTShowTopNum"
        kv=f'{key}="{text}"'
        change=""
        configs = read("str")    
        if kv not in configs:
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)                
                write(configs)
            else:
                configs = read("str")
                configs += f'export {key}="{text}"\n'                
                write(configs)
            change = f'已替换屏蔽京豆数为{text}' 
        else:
            change = f'设定没有改变,想好再来.' 
            
        await event.edit(change)
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
@user.on(events.NewMessage(pattern=r'^bd', outgoing=True))
async def CCBeanDetailInfo(event):
    msg_text= event.raw_text.split(' ')
    if len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: cb 1 或 cb ptpin')
        return    
        
    key="BOTCHECKCODE"
    kv=f'{key}="{text}"'
    change=""
    configs = read("str")    
    intcount=0
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
                

    await event.edit('开始查询账号'+text+'的资产，请稍后...')
        
    cmdtext="task /ql/repo/ccwav_QLScript2/bot_jd_bean_info_QL.js now"        
    p = await asyncio.create_subprocess_shell(
        cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    res_bytes, res_err = await p.communicate()
    res = res_bytes.decode('utf-8') 
    txt=res.split('\n')
    strReturn="" 
    await event.delete()
    if res:
        for line in txt:                
            if "【" in line and "🔔" not in line:
                strReturn=strReturn+line+'\n'
            if intcount==100:
                intcount=0
                if strReturn:                    
                    await user.send_message(event.chat_id, strReturn)
                    strReturn="" 
    else:
        await user.send_message(event.chat_id,'查询失败!')
        
    if strReturn:        
        await user.send_message(event.chat_id, strReturn)
    