cd /
mkdir kcp
cd kcp
wget https://github.com/xtaci/kcptun/releases/download/v20190109/kcptun-linux-amd64-20190109.tar.gz
tar -zxvf kcptun-linux-amd64-20190109.tar.gz
git clone https://github.com/chu8129/marks
cp marks/kcp.proxy.py ./proxy.py
rm -rf marks
touch start.sh

chmod +x start.sh
echo "*/5 * * * * /kcp/start.sh" >> /var/spool/cron/root



#!/bin/bash
while true
do
    kill1="ps -ef|grep proxy.py|awk '{print \$2}'|xargs kill -9"
    ps1="ps -ef|grep proxy"
    no1="nohup python proxy.py 8132 1>/dev/null 2>&1 &"
    kill2="ps -ef|grep server_linux_amd64|awk '{print \$2}'|xargs kill -9"
    no2="nohup ./server_linux_amd64 -t localhost:8132 -l :8131 -mode fast3 -mtu=512 1>/dev/null 2>&1 &"
    ps2="ps -ef|grep server_linux_amd64"
    eval $kill1
    eval $ps1
    eval $no1
    eval $kill2
    eval $no2
    eval $ps2
    s="sleep 600"
    eval $s
done
