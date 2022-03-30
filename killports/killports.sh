#!/bin/sh

killbyport()
{
    proccess=`lsof -i:$1 2>/dev/null`
    if [ ! -n "$proccess" ];then
        echo -e "\033[33mwarning\033[0m: can't find proccess with open port $1"
        return 1
    fi

#    lines=`echo "$proccess" | wc -l`
#    if [ $lines -le "2" ];then
#        echo -e "\033[33mwarning\033[0m: find more than one proccess open port $1"
#        return 2
#    fi

    pid=`echo "$proccess" | tail -n 1 | awk '{print $2}'`

    kill -9 $pid 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "\033[32msuccess\033[0m: kill open port $1 proccess $pid"
    else
        echo -e "\033[31mfailed\033[0m: kill open port $1 proccess $pid"
    fi

    return 0
}

if [ $# -eq 0 ];then
    echo -e "\033[31musage:\033[0m killports port1 [port2 ...]\n"
fi

for port in "$@"
    do
        killbyport $port
done
