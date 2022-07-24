from telethon import events
from .. import user
from ..diy.utils import read
import re
import requests
@user.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    configs = read("str")    
    M_API_TOKEN = ""
    if "M_API_TOKEN" in configs:
        TempConfigs = configs.split("\n")
        for config in TempConfigs:
            if "M_API_TOKEN" not in config:                
                continue            
            kv = config.replace("export ", "")
            M_API_TOKEN = re.findall(r'"([^"]*)"', kv)[0]
            
    if len(M_API_TOKEN) == 0:
        await user.send_message(event.chat_id,"请先找 @magic_noyify_bot 申请解析token填入青龙变量,关键字为M_API_TOKEN")
        return 
            
    headers = {"token": M_API_TOKEN}
    strText=""
    if event.is_reply is True:
        reply = await event.get_reply_message()
        strText=reply.text
    else:    
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]
    
    if strText==None:
        await user.send_message(event.chat_id,'请指定要解析的口令,格式: jx 口令 或对口令直接回复jx ')
        return    
        
    data = requests.post("http://ailoveu.eu.org:19840/jCommand",
                             headers=headers,
                             json={"code": strText}).json()
    code = data.get("code")
    if code == 200:
        data = data["data"]
        title = data["title"]
        jump_url = data["jumpUrl"]
        await user.send_message(event.chat_id,title+"\n"+jump_url)
    else:
        await user.send_message(event.chat_id,"解析出错:"+data.get("data"))
    
    