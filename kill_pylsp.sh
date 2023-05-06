#!/bin/bash
 
# 获取指定进程所运行的时间
function checkProcessRuntime(){
# name=$1
base_path=$(cd `dirname "$0"`;pwd)
cd "${base_path}"

# 读取配置文件
config=$(cat params.properties)
log_path=$(echo "${config}" | grep "^log_path=" | cut -d'=' -f2)
record_path=$(dirname $log_path)/language-server-kill-record.log

current_time=$(date "+%Y.%m.%d-%H:%M:%S")

cur_pid=$$
sys_uptime=$(cat /proc/uptime | cut -d" " -f1)
user_hz=$(getconf CLK_TCK)
base_name=$(basename $BASH_SOURCE)
echo "base_name:" + $base_name
echo -e "\033[32mpid runtime(seconds)\033[0m"
for pid in `ps aux | grep pylsp | egrep -v "grep|$base_name" | awk '{print $2}' | sed "/$cur_pid/d"`
do
  if [[ ! -z $pid && -f /proc/$pid/stat ]]
    then
    # start_time=$(ps -p $pid -o lstart)
    up_time=$(cat /proc/$pid/stat | cut -d" " -f22)
    run_time=$((${sys_uptime%.*}-$up_time/$user_hz))
    if [ ${run_time} -ge 7200 ];then
            echo -e "[${current_time}][python-language-server][kill_pylsp] kill pylsp process pid start more than 2 hours process id: ${pid}" |tee -a ${record_path}
            kill -15 $pid
    fi
    echo "${pid} ${run_time}"
  fi
done

}

checkProcessRuntime