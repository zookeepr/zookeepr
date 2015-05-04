#!/bin/bash

while IFS=, read id ready c3 c4 c5 c6
do
    #echo "I got:$id|$c5"
    #URL=`echo $c5 | sed "s/^,//"`
    if [ "$ready" -ge "11" ]
    then
        #echo "UPDATE schedule set video_url='$c6' where id='$c4';"
	#echo "$c6"
	#echo "$c4"
	URL=`echo $c6 | sed s///`
        #echo "UPDATE schedule set video_url='$c6' jj"
        #echo "UPDATE schedule set video_url='$c6' where id='$c4';"
        echo "UPDATE schedule set video_url='$URL' where id='$c4';"
    fi
done < lca_2015.csv
