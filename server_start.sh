#!/bin/bash
# p_version=$1

function run(){
    echo "check server port 3001"
    port_status=`netstat -nlt|grep 3001|wc -l`
    base_path=$(cd `dirname $0`;pwd)
    if [ $port_status -gt 0 ]
    then
        echo "端口已被占用，即将调用server_stop.sh脚本停止服务"
        sh ./server_stop.sh
    fi
    echo "begin to start server..."
    nohup ${base_path}/bin/python3 -u python-server/langserver_ext.py > /appcom/logs/dssInstall/python-language-server.log 2>&1 &
    sleep 5s
    echo "python server start finished!"
}

run 
