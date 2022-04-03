#!/usr/bin/env bash
set -e

daili='https://git.metauniverse-cn.com/'

install_depend(){
    echo -e "\n1.开始安装所需依赖\n"
    echo -e "#机器人所需依赖" >>/ql/config/extra.sh
    # 包依赖
    apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers
    # 模块依赖
    pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0

    if [ `grep "#机器人所需依赖" /ql/config/extra.sh` ];then
        echo "已设置重启青龙自动启动机器人"
    else
        echo -e "解决重启青龙后，jbot失效问题~"
        echo 'apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers' >>/ql/config/extra.sh
        echo 'pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0' >>/ql/config/extra.sh
        echo 'cd /ql/jbot  && pm2 start ecosystem.config.js' >>/ql/config/extra.sh
        echo 'cd /ql/ && pm2 start jbot' >>/ql/config/extra.sh
    fi

}

gitPull(){
    echo -e "\n2.开始拉取所需代码\n"
    if [ ! -d /ql/jbot ]; then
        mkdir /ql/jbot
    else
        rm -rf /ql/jbot/*
    fi

    if [ ! -d /ql/scripts ];then
        # 青龙新版文件路径
        ln -sf /ql/data/scripts /ql/
    fi

    cd /ql/repo && git clone ${daili}https://github.com/curtinlv/gd.git
    cp -a /ql/repo/gd/* /ql/jbot && cp -a /ql/jbot/conf/* /ql/config && cp -a /ql/jbot/jk_script/* /ql/scripts
    rm -rf /ql/repo/dockerbot
    mkdir /ql/repo/dockerbot && ln -sf /ql/repo/gd /ql/repo/dockerbot/jbot
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
    echo -e "如果需要重新部署，请复制以下命令执行："
    echo -e "\nrm -rf  /ql/jbot/*  &&   bash  install.sh\n"
    exit 0
fi
install_depend
gitPull
echo -e "\n*******************\n所需环境已部署完成\n*******************\n"
echo -e "请配置tg机器人参数，再启动机器人即可。\n参考本仓库第3-4步:\nhttps://github.com/curtinlv/gd/blob/main/README.md "
