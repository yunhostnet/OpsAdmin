#!/bin/bash
#Auth:zp
#Created:2016.02.02

WORKING_DIR=$(dirname "$0")
export WORKING_DIR=$(cd -P "$WORKING_DIR"/ > /dev/null; pwd)

app=""

MEM_INFO=$(cat /proc/meminfo  | grep MemTotal | awk '{print$2}')
DISK_INFO=$(/sbin/fdisk -l |grep Disk | grep bytes  | awk '{print$2,$3,$4}'|tr ',\n' ' ')
CPU_INFO=$(cat /proc/cpuinfo | grep processor | wc -l)
MAC=$(ifconfig -a | grep eth0 | awk '{print$NF}')
SYSTEM=$(cat /etc/redhat-release | cut -d " " -f1,3)

echo "mem_info;$MEM_INFO,cpu_info;$CPU_INFO,mac;$MAC,system;$SYSTEM,disk_info;$DISK_INFO"
