#!/bin/bash
echo -e "python server will be stopped"
echo -e "kill server port 3001"
for SERVER_PID in $(netstat -nlp | grep :3001 | awk '{print $7}' | awk -F'/' '{print $1}' | sort -u);
  do
    echo "language server process id: ${SERVER_PID}";
    kill -9 ${SERVER_PID};
done

cur_pid=$$
base_name=$(basename $BASH_SOURCE)
echo -e "check pylsp process"
for PYLSP_PID in `ps aux | grep pylsp | egrep -v "grep|$base_name" | awk '{print $2}' | sed "/$cur_pid/d"`
 do
   echo -e "pylsp process id: " ${PYLSP_PID};
   kill -9 ${PYLSP_PID};
done

echo "..."
sleep 3s
echo -e "python server stop completion"

