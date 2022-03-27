



<h1 align="center">
  青龙安装Bot监控
  <br>
</h1>


## 1.进入容器内

``` bash
# 进入青龙容器内，“qinglong” 为容器名字。
docker exec -it qinglong /bin/bash
```

## 2.安装依赖

- [x] 一键安装

```
wget https://raw.githubusercontent.com/curtinlv/gd/main/install.sh && bash install.sh
```

- [ ] 人工安装

``` bash
# 操作环境，容器内执行。如果一键安装完成，就不用执行这一块。
# 包依赖
apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers

# 模块依赖
pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0

# 拉取jbot主要代码
cd /ql/repo && git clone https://github.com/curtinlv/gd.git
cp -a /ql/repo/gd/* /ql/jbot && cp -a /ql/jbot/conf/* /ql/config 
cp -a /ql/jbot/jk_script/* /ql/scripts
mkdir /ql/log/bot

```



## 3.配置tg机器人参数

```bash
# 操作环境，容器内:
# 机器人登录相关参数，存放路径：
## 填写参考：https://raw.githubusercontent.com/curtinlv/gd/main/conf/bot.json
vi /ql/config/bot.json

# 监控频道相关参数，存放路径：
## 填写参考：https://raw.githubusercontent.com/curtinlv/gd/main/conf/botset.json
vi /ql/config/diybotset.json

```



## 4.启动机器人

```bash
# 操作环境，容器内:
## 删除历史登录session
rm -f /ql/config/user.session

# 首次启动，按照提示登录tg，填手机号格式0086xxxxxxxx
cd /ql
python3 -m jbot

```

![图1：首次登录授权个人tg](https://raw.githubusercontent.com/curtinlv/gd/main/img/p1.png)

### ∆出现以上提示，即登录成功，按`ctrl+c `终止，继续以下操作：

```bash
# 通过pm2 后台启动，除了登录验证外，建议使用pm2启动机器人
cd /ql/jbot/
pm2 start ecosystem.config.js #第一次启动是这样启动，后续启动参考底部相关命令

# 查看日志：看看有没有报错。
tail -100f /ql/log/bot/run.log
#终止查看日志 按 Ctrl+C


```

​																

- [x] 如tg机器人给你发以下信息，证明你填写的机器人参数是正确的∆。

![图2：完成登录，tg机器人发通知](https://raw.githubusercontent.com/curtinlv/gd/main/img/p2.png)

- [x] 发送【user?】 给你的机器人，有以下回复，证明你通过号码成功授权登录。

![图3：测试1](https://raw.githubusercontent.com/curtinlv/gd/main/img/p3.png)

- [x] 在所监控的频道发出变量，机器人会马上通知：

![图4：测试2](https://raw.githubusercontent.com/curtinlv/gd/main/img/p4.png)



<h1 align="center">
  恭喜你，部署已完成。
  <br>
</h1>






```bash
#################### 相关命令 ####################
操作环境：进入容器内
## 查看机器人运行状态
pm2 status jbot

## 启动机器人：
pm2 start jbot

## 停止机器人
pm2 stop jbot

## 重启机器人
pm2 restart jbot

## 更新监控脚本：
1.把新增的脚本发给机器人，仅保存到 scripts 目录下
2.更新user.py 监控，给机器人发送指令（直接复制整行，不能换行）
/cmd  cd  /ql/jbot/user/ && rm -f user.py && wget https://raw.githubusercontent.com/curtinlv/gd/main/user/user.py
3.重启生效，给机器人发送指令
/reboot

```



# 特别感谢
- 脚本的写作参考了:
  - [SuMaiKaDe](https://github.com/SuMaiKaDe) 的 [bot](https://github.com/SuMaiKaDe/bot) 仓库
  - [chiupam](https://github.com/chiupam) 的 [JD_Diy](https://github.com/chiupam/JD_Diy) 仓库
  - [msechen](https://github.com/msechen) 的 [jdrain](https://github.com/msechen/jdrain) 仓库
  - 未完待定
