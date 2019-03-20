cd /
mkdir kcp
cd kcp
wget https://github.com/xtaci/kcptun/releases/download/v20190109/kcptun-linux-amd64-20190109.tar.gz
tar -zxvf kcptun-linux-amd64-20190109.tar.gz
git clone https://github.com/chu8129/marks
cp marks/kcp.proxy.py ./proxy.py
rm -rf marks
touch start.sh
echo "ps -ef|grep proxy.py|awk '{print $2}'|xargs kill -9" >> start.sh
echo "nohup python proxy.py 8132 1>/dev/null 2>&1 &" >> start.sh
echo "ps -ef|grep server_linux_amd64|awk '{print $2}'|xargs kill -9" >> start.sh
echo "nohup ./server_linux_amd64 -t localhost:8132 -l :8131 -mode fast3 -mtu=512 1>/dev/null 2>&1 &" >> start.sh
echo "ps -ef|grep server_linux_amd64" >> start.sh
chmod +x start.sh
echo "*/5 * * * * /kcp/start.sh" >> /var/spool/cron/root
