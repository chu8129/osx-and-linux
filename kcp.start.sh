https://github.com/chu8129/marks/edit/master/proxy.py

ps -ef|grep proxy.py|awk '{print $2}'|xargs kill -9
nohup python proxy.py 8132 1>/dev/null 2>&1 &
ps -ef|grep server_linux_amd64|awk '{print $2}'|xargs kill -9 
nohup ./server_linux_amd64 -t localhost:8132 -l :8131 -mode fast3 -mtu=512 1>/dev/null 2>&1 &
ps -ef|grep server_linux_amd64
