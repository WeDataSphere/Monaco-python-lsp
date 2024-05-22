#!/bin/bash

echo -e "python server will be stopped"

base_path=$(cd `dirname "$0"`;pwd)
# shellcheck disable=SC2164
cd "${base_path}"
echo -e "current path: ${base_path}"

# 读取配置文件
config=$(cat params.properties)

# 解析 JSON 数据
server_port=$(echo "${config}" | grep "^server_port=" | cut -d'=' -f2)
log_path=$(echo "${config}" | grep "^log_path=" | cut -d'=' -f2)
record_path=$(dirname $log_path)/language-server-kill-record.log

#echo -e "python server will be stopped"
#echo -e "kill server port ${server_port}"
#if [ -z ${server_port} ]; then
#   echo -e "server port is empty, server will exit"
#   exit 1
#fi

current_time=$(date "+%Y.%m.%d-%H:%M:%S")

for SERVER_PID in `ps aux | grep python-server/langserver_ext.py| egrep -v "grep" | awk '{print $2}'`
  do
    echo -e "[${current_time}][python-language-server] kill process id: ${SERVER_PID}" |tee -a ${record_path}
    if [ -z "$SERVER_PID" ]; then
       continue
    fi
    echo "kill server process ${SERVER_PID}"
    kill -15 "${SERVER_PID}";
done

echo -e "check pylsp process"
# shellcheck disable=SC2006
# shellcheck disable=SC2009
# shellcheck disable=SC2196
for PYLSP_PID in `ps aux | grep pylsp | egrep -v "grep" | awk '{print $2}'`
 do
   echo -e "[${current_time}][python-language-server] kill pylsp process id: ${PYLSP_PID}" |tee -a ${record_path}
   if [ -z "$PYLSP_PID" ]; then
       continue
   fi
   echo "kill pylsp process ${PYLSP_PID}"
   kill -15 ${PYLSP_PID};
done

echo -e "python server stop completion"