#!/bin/sh

ps aux | grep a1 | head -1 | awk '{print $2}' | xargs -i kill -9 {}
cd /home/gm/temp

today=`date +%Y-%m-%d`

if [ ! -d $today ]
then
	mkdir $today
fi

find . -maxdepth 1 -name '*.jpg' -type f -cmin -30  | xargs -i mv -f {} ./$today/ >> /dev/null
