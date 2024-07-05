#!/bin/bash

function run(){

    # shellcheck disable=SC2046
    # shellcheck disable=SC2164
    # shellcheck disable=SC2006
    base_path=$(cd `dirname "$0"`;pwd)
    # shellcheck disable=SC2164
    cd "${base_path}"

    # 读取配置文件
    config=$(cat params.properties |tr -d '\r')

    # 解析 JSON 数据
    log_file=$(echo "${config}" | grep "^log_path=" | cut -d'=' -f2)
    server_port=$(echo "${config}" | grep "^server_port=" | cut -d'=' -f2)

    echo "check server port ${server_port}"
    # shellcheck disable=SC2126
    # shellcheck disable=SC2006
    port_status=`netstat -nlt|grep "${server_port}"|wc -l`

    if [ "$port_status" -gt 0 ]
    then
        echo "端口已被占用，即将调用server_stop.sh脚本停止服务"
        sh ./server_stop.sh
    fi

    echo "begin to start server..."
    # 标准输出重定向到/dev/null，标准错误输出重定向到log_file日志文件中
    nohup ./bin/python3 -u ./python-server/langserver_ext.py > /dev/null 2>> "${log_file}" &
    sleep 3s
    echo "python server start finished!"

    tail -n 5 "${log_file}"
    echo "log path: ${log_file}"
}

run