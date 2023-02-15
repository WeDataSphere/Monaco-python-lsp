#!/bin/bash
p_version=$1

function run(){
    echo "check server port 3001"
    port_status=`netstat -nlt|grep 3001|wc -l`
    if [ $port_status -gt 0 ]
    then
        echo "端口已被占用，即将调用server_stop.sh脚本kill进程"
        sh ./server_stop.sh
    fi
    server_start
}

function server_start(){
    echo "python server will to be start..."
    echo "server port 3001"
    if [ ! $p_version ]; then
        echo "未指定python版本：python3/Python3 eg:sh server_start.sh python3"
        echo "服务未启动"
    else
        case $p_version in
            "python3") 
                 nohup $p_version -u python-server/langserver_ext.py > /appcom/logs/dssInstall/python-language-server.log 2>&1 &
                 sleep 5s
                 echo "python server start finished!"
            ;;
            "Python3")  
                 nohup $p_version -u python-server/langserver_ext_p.py > /appcom/logs/dssInstall/python-language-server.log 2>&1 &
                 sleep 5s
                 echo "python server start finished!"
            ;;
            *)  echo 'python版本错误请输入：python3/Python3'
            ;;
        esac
    fi
}

run $1
