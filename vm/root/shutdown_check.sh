#!/bin/sh

# set -x

threshold=1200

HOLDFILE=/home/brian/hold
EPOCH=$(date '+%s')

# Check if the system has been up longer than 900s
uptime=$(awk '{print int($1)}' /proc/uptime)
if [ $uptime -lt $threshold ]; then
    exit 0
elif [ -n "$(find /home/brian/torrents/active -type f)" ]; then
    exit 0
elif [ -n "$(find /home/brian/torrents/torrent_files/active -type f)" ]; then
    exit 0
elif [ -n "$(find /home/brian/torrents/torrent_files/staging -type f -name *.torrent)" ]; then
    wall "UTServer isn't running"
    exit 0
elif [ -n "$(find /home/brian/torrents/done -type f)" ]; then
    exit 0
elif [ -f $HOLDFILE ]; then
    holdtime=$(cat $HOLDFILE)
    if [ $EPOCH -lt $holdtime ]; then
    	exit 0
    fi
fi

# Cleanup torrent files
actv="$(find /home/brian/torrents/active -mindepth 1 -type d -empty -print -delete)"
done="$(find /home/brian/torrents/done -mindepth 1 -type d -empty -print -delete)"
stag="$(find /home/brian/torrents/torrent_files/staging -type f -print -delete)"
file="$(find /home/brian/torrents/torrent_files/done -type f -print -delete)"

uptime=$(awk '{x=$1; h=int(x/3600); m=int(x/60)-h*60; s=x-m*60-h*3600; printf("%02dh%02dm%02ds\n", h, m, s)}' /proc/uptime)
printf "Pimpbox was up for $uptime\n$actv\n$done\n$stag\n$file\n" |  mail -s "Pimpbox Shutting Down" -a "From: barbituate@gmail.com" barbituate@gmail.com

/sbin/shutdown 3 > /dev/null 2>&1
exit 0
