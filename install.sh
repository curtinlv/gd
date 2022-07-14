#!/usr/bin/env bash
set -e

daili=''

if [ -d /ql/data/config ];then
    QLMainPath='/ql/data'
else
    QLMainPath='/ql'
fi
echo -e "\n\t\t\t你的青龙版本为:${QL_BRANCH}\n"

install_depend(){

    echo -e "\n1.开始安装所需依赖\n"
    # 包依赖
    apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers
    # 模块依赖
    pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0

    if [ -f ${QLMainPath}/config/extra.sh ];then
        if [ `grep "#机器人所需依赖" ${QLMainPath}/config/extra.sh` ];then
            echo "已设置重启青龙自动启动机器人"
        else
            echo -e "解决重启青龙后，jbot失效问题~"
            echo -e "#机器人所需依赖" >>${QLMainPath}/config/extra.sh
            echo "apk add zlib zlib-dev libjpeg-turbo libjpeg-turbo-dev gcc python3-dev libffi-dev musl-dev linux-headers" >>${QLMainPath}/config/extra.sh
            echo "pip3 install qrcode==7.3.1 Telethon==1.24.0 requests==2.27.1 Pillow==9.0.0 python-socks==1.2.4 async_timeout==4.0.2 prettytable==3.0.0" >>${QLMainPath}/config/extra.sh
            echo "cd ${QLMainPath}/jbot  && pm2 start ecosystem.config.js" >>${QLMainPath}/config/extra.sh
            echo "cd ${QLMainPath}/ && pm2 start jbot" >>${QLMainPath}/config/extra.sh
        fi
    fi

}

gitPull(){
    echo -e "\n2.开始拉取所需代码\n"
    if [ ! -d ${QLMainPath}/jbot ]; then
        mkdir ${QLMainPath}/jbot
    else
        rm -rf ${QLMainPath}/jbot/*
    fi
    cd ${QLMainPath}/repo && rm -rf gd && git clone ${daili}https://github.com/curtinlv/gd.git
    cp -a ${QLMainPath}/repo/gd/* ${QLMainPath}/jbot && cp -a ${QLMainPath}/jbot/conf/* ${QLMainPath}/config && cp -a ${QLMainPath}/jbot/jk_script/* ${QLMainPath}/scripts
    rm -rf ${QLMainPath}/repo/dockerbot
    mkdir ${QLMainPath}/repo/dockerbot && ln -sf ${QLMainPath}/repo/gd ${QLMainPath}/repo/dockerbot/jbot && ln -sf ${QLMainPath}/repo/gd/conf ${QLMainPath}/repo/dockerbot/config
    if [ ! -d ${QLMainPath}/log/bot ]; then
        mkdir ${QLMainPath}/log/bot
    fi

}

# start

echo
echo -e "\n\t\t\t【青龙安装Bot监控】\n"
echo
if [ -f ${QLMainPath}/jbot/user/user.py ];then
    echo -e "\n你已部署，请启动即可:\ncd ${QLMainPath}\npython3 -m jbot\n\n或参考本仓库第3-4步:\nhttps://github.com/curtinlv/gd/blob/main/README.md"
    echo -e "如果需要重新部署，请复制以下命令执行："
    echo -e "rm -rf  ${QLMainPath}/jbot/*  &&   bash  install.sh\n"
    exit 0
fi
install_depend
gitPull
echo -e "\n*******************\n所需环境已部署完成\n*******************\n"
echo -e "请前往面板【配置文件】配置tg机器人参数，再启动机器人即可。\n参考本仓库第3-4步: https://github.com/curtinlv/gd/blob/main/README.md "
