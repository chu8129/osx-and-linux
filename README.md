# osx-and-linux
更改路由表
route delete 0.0.0.0
route add -net 0.0.0.0 192.168.100.10
route add -net 188.5.0.0 188.5.63.1 -netmask 255.255.0.0
