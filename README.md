# osx-and-linux
更改路由表

route delete 0.0.0.0

route add -net 0.0.0.0 192.168.100.10

route add -net 188.5.0.0 188.5.63.1 -netmask 255.255.0.0

SCP

eval $(find .  -name "*bz2" -print|awk '{print "scp "$0" root@188.*.**.27:/Users/**/Desktop/"}')


ssh -CNfR 远程端口:本地ip/代理的ip:本地端口/代理端口 远程账号@远程ip
