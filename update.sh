#!/usr/bin/env bash
set -e

daili='https://ghproxy.com'

if [ -d /ql/data/config ];then
    QLMainPath='/ql/data'
else
    QLMainPath='/ql'
fi
echo -e "当前青龙版本为:${QL_BRANCH}\n"

gitPull(){
    echo -e "\n开始更新gd机器人\n"
    rm -rf ${QLMainPath}repo/dockerbot/*
    rm -rf ${QLMainPath}/repo/gd
    cd ${QLMainPath}/repo/ && git clone ${daili}/https://github.com/curtinlv/gd.git
    if [ ! -d ${QLMainPath}/repo/dockerbot ];then
        mkdir ${QLMainPath}/repo/dockerbot
    fi
    ln -sf ${QLMainPath}/repo/gd ${QLMainPath}/repo/dockerbot/jbot
    ln -sf ${QLMainPath}/repo/gd/conf ${QLMainPath}/repo/dockerbot/config
    pm2 stop jbot && rm -rf ${QLMainPath}/jbot/* && cp -a ${QLMainPath}/repo/gd/* ${QLMainPath}/jbot/ && pm2 start jbot
}

# start

echo
echo -e "\n\t\t\t【更新机器人】\n"
echo
gitPull
echo -e "已完成更新"

