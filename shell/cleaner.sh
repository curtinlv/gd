#!/usr/bin/env bash

# 清理垃圾

fun_clean(){
    daynum=${1}
    if [ -d /ql ];then
        if [ -d /ql/data/config ];then
            QLMainPath='/ql/data'
         else
            QLMainPath='/ql'
        fi
        echo -e "当前青龙版本:${QL_BRANCH}\n"
        logUse=`du -sh ${QLMainPath}/log`
        echo -e "日志目录使用情况:\n\t${logUse}"
        echo -e "\t-开始清理【$daynum】天前的日志文件"
        find ${QLMainPath}/log -type f -name "*.log" -mtime +${daynum} -exec rm -f {} \;
        echo -e "\t-开始清理缓存文件core.xxxx"
        find ${QLMainPath} -name "core.*[0-9]" -exec rm -f {} \;
    fi

    if [ -d /jd ];then
        echo -e "开始清理缓存文件core.xxxx"
        find /jd -name "core.*[0-9]" -exec rm -f {} \;
    fi
    echo -e "完成清理"
}

cxkj(){
    echo
    echo -e "-----------------\n当前空间："
    Size=`df -h | grep '/$' | awk '{print $2}'`
    Used=`df -h | grep '/$' | awk '{print $3}'`
    Use=`df -h | grep '/$' | awk '{print $5}'`
    echo -e "总量 \`${Size}\`\n已用 \`${Used}\`\n用率 \`${Use}\`"
    echo -e "-----------------"

}

fun_clean $1
cxkj