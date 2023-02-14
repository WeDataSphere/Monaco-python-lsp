#!/bin/bash
echo "python server will to be start..."
echo "server port 3001"
nohup python3 -u python-server/langserver_ext.py > /appcom/logs/dssInstall/python-language-server.log 2>&1 &
sleep 5s
echo "python server start finished!"
