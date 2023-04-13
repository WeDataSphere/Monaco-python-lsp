#!/bin/bash

function run(){

    base_path=$(cd `dirname $0`;pwd)
    cd ${base_path}

    # 读取配置文件
    config=$(cat params.properties)

    # 解析 JSON 数据
    log_file=$(echo "${config}" | grep "^log_path=" | cut -d'=' -f2)
    server_port=$(echo "${server_port}" | grep "^server_port=" | cut -d'=' -f2)

    echo "check server port ${server_port}"
    port_status=`netstat -nlt|grep ${server_port}|wc -l`

    if [ $port_status -gt 0 ]
    then
        echo "端口已被占用，即将调用server_stop.sh脚本停止服务"
        sh ./server_stop.sh
    fi

    echo "begin to start server..."
    nohup ./bin/python3 -u ./python-server/langserver_ext.py > /dev/null 2>&1 &
    sleep 3s

    tail -n 5 ${log_file}

    echo "log path: ${log_file}"
    echo "python server start finished!"
}

run