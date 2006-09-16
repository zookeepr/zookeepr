#!/bin/bash

# path of MoinMoin shared files
SHARE=/usr/share/moin

# path to target instance location
INSTANCE=$1

# should be nice
USER=www-data
GROUP=www-data

if [ ! $1 ]
then
  echo "You must specify an instance (relative or absolute path)"
  exit
fi

if [[ -e $1 || -d $1 ]]
then
  echo "$1 already exists"
  exit
fi

mkdir -p $INSTANCE
cp -R $SHARE/data $INSTANCE
cp -R $SHARE/underlay $INSTANCE
cp $SHARE/config/wikiconfig.py $INSTANCE

chown -R $USER.$GROUP $INSTANCE
chmod -R ug+rwX $INSTANCE
chmod -R o-rwx $INSTANCE

if [ $? ]
then
  echo "Done."
fi

