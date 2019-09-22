#!/bin/bash -e
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPTPATH

for i in $(ls -d */ | tr '/' ' ')
do
    for j in $(ls $i/ )
    do
        echo -e "\n==> Processing docker image $i:$j"
        make -f ../Makefile image-build TARGET_DIR=$i DOCKERFILE=$j
    done
done