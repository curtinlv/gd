#!/usr/bin/env bash
set -e

install_depend(){
    echo -e "\n1.开始安装所需依赖\n"
    # 包依赖
    apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers
    # 模块依赖
    pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0
}

gitPull(){
    echo -e "\n2.开始拉取所需代码\n"
    if [ ! -d /ql/jbot ]; then
        mkdir /ql/jbot
    fi
    cd /ql/repo && git clone https://github.com/curtinlv/gd.git
    cp -a /ql/repo/gd/* /ql/jbot && cp -a /ql/jbot/conf/* /ql/config && cp -a /ql/jbot/jk_script/* /ql/scripts
    if [ ! -d /ql/log/bot ]; then
        mkdir /ql/log/bot
    fi

}

# start

echo
echo -e "\n\t\t\t【青龙安装Bot监控】\n"
echo
if [ -f /ql/jbot/user/user.py ];then
    echo -e "\n你已部署，请启动即可:\ncd /ql\npython3 -m jbot\n\n或参考本仓库第3-4步:\nhttps://github.com/curtinlv/gd/blob/main/README.md\n"
    exit 0
fi
install_depend
gitPull
echo -e "\n*******************\n所需环境已部署完成\n*******************\n"
echo -e "请配置tg机器人参数，再启动机器人即可。\n参考本仓库第3-4步:\nhttps://github.com/curtinlv/gd/blob/main/README.md "
