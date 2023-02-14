#!/bin/bash
 
# 获取指定进程所运行的时间
function checkProcessRuntime(){
# name=$1
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
    if [ ${run_time} -ge 60 ];then
            echo 'pylsp process pid start more than 2 hours:' $pid
            kill -9 $pid
    fi       
    echo "${pid} ${run_time}"
  fi
done
 
}
 
checkProcessRuntime 
