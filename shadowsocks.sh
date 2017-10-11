wget --no-check-certificate -O shadowsocks.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks.sh
chmod +x shadowsocks.sh
./shadowsocks.sh 2>&1 | tee shadowsocks.log
https://twitter.com/clowwindy
https://teddysun.com/342.html


{
    "server":"0.0.0.0",
    "server_port":8129,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":true,
    "workers": 1
}
