#!bin/sh

# 参数1：镜像名称 参数2：网络名称 参数3：IP地址

# 指定网络和ip启动镜像，判断如果没输入参数或者输入部分参数如何启动
if [ -z "$2" ]
then
   docker run -p 8081:8080 -dit -v /root/docker_practice/run.sh:/home/work/webapps/run.sh $1
   exit
else
   docker run -dit -p 8081:8080 --net $2 --ip $3 /root/docker_practice/run.sh:/home/work/webapps/run.sh $1
fi