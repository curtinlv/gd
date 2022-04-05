#!/bin/bash
set -e

gitPull(){
    echo -e "\n开始更新gd机器人\n"
    rm -rf /ql/repo/gd
    cd /ql/repo/
    echo "cd /ql/repo/"
    /usr/bin/git clone https://git.metauniverse-cn.com/https://github.com/curtinlv/gd.git
    echo "/usr/bin/git clone https://git.metauniverse-cn.com/https://github.com/curtinlv/gd.git"
    rm -rf /ql/repo/dockerbot
    mkdir /ql/repo/dockerbot
    ln -sf /ql/repo/gd /ql/repo/dockerbot/jbot
    /usr/local/bin/pm2 stop jbot
    rm -rf /ql/jbot/*
    cp -a /ql/repo/gd/* /ql/jbot/
    /usr/local/bin/pm2 start jbot
}

# start

echo
echo -e "\n\t\t\t【更新机器人】\n"
echo
gitPull
echo -e "已完成更新"
