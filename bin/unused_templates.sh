#!/bin/bash

TEMPLATES=`find zkpylons/templates/ -type 'f' | sed 's/zkpylons\/templates//'`

for TEMPLATE in $TEMPLATES
do
	USERS=`grep -R --binary-files=without-match -F -l "$TEMPLATE" zkpylons/`
	if [ -z "$USERS" ]; then
		SERS=`grep -R --binary-files=without-match -F -l "${TEMPLATE:1}" zkpylons/`
		if [ -z "$SERS" ]; then
			TCMD="grep -R --binary-files=without-match -F -l `basename $TEMPLATE` zkpylons/templates`dirname $TEMPLATE`"
			TEASERS=`$TCMD`
			if [ -z "$TEASERS" ]; then
				echo "$TEMPLATE"
			fi
		fi
	fi
done
