from telethon import events
# from .login import user
import requests
from .. import jdbot, user
import json

@user.on(events.NewMessage(pattern=r'.*天气$', outgoing=True))
async def weatherInfo(event):
    
    message = event.message.text.split("天气")[0]
    if message==None:
        await event.edit('请输入正确的格式如:深圳天气')
        return
    
    #旧接口
    # url='https://www.tianqiapi.com/api/?version=v6&appid=74169348&appsecret=ti3VzXtb&city=%s'%message   
    # try:
        # weather_data=json.loads(requests.get(url).text)        
    # except Exception as e:
        # await user.send_message(event.chat_id,"获取天气信息错误:"+e)
        # return
        
    # if weather_data and (weather_data['city']==message or (weather_data['city']!="北京")):
        # await user.send_message(event.chat_id,'当前城市：'+weather_data['city']+'\n更新时间：'+weather_data['update_time']+'\n建议：'+weather_data['air_tips']+'\n温度：'+weather_data['tem']+'℃\n风速：'+weather_data['win_speed']+'\n风力：'+weather_data['win_meter']+'\n风向：'+weather_data['win']+'\n天气：'+weather_data['wea'])
    # else:
        # await user.send_message(event.chat_id,'获取天气信息错误,可能输入的城市有误或不被支持!')    
        
        
    url='http://hm.suol.cc/API/tq.php?msg='+message+'&n=1'
    try:
        weather_data=requests.get(url).text
    except Exception as e:
        await user.send_message(event.chat_id,"获取天气信息错误:"+e)
        return
    strweatherinfo=""
    strotherinfo=""
    lncount=0
    weatherinfos=weather_data.split("\n")
    for weatherline in weatherinfos:
        lncount=lncount+1
        if "：" in weatherline:
            Title=weatherline.split("：")[0]
            if Title=="预警信息":
                strweatherinfo+=weatherline.replace("预警信息：","")+"\n"
            else:
                strweatherinfo+="【"+Title+"】 "+weatherline.split("：")[1]+"\n"
        else:
            if lncount==1:
                strweatherinfo+="【位置】 "+weatherline+"\n"
            else:
                if strotherinfo!="":
                    strotherinfo+="\n"
                strotherinfo+=weatherline
                
    
    if strotherinfo!="":
        strweatherinfo+="【温馨提示】"+strotherinfo
        
    if strweatherinfo !="" :
        await user.send_message(event.chat_id,strweatherinfo)
    else:
        await user.send_message(event.chat_id,'获取天气信息错误,可能输入的城市有误或不被支持!')