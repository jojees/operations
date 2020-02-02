#!/bin/bash -e
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
cd $SCRIPTPATH

BUILD=1

while getopts "pd" opt
do
    case $opt in
    (p) PUSH=1 ;;
    (d) BUILD=0 ;;
    (*) printf "Illegal option '-%s'\n" "$opt" && exit 1 ;;
    esac
done

#for i in $(ls -d */ | tr '/' ' ')
#do
#    for j in $(ls $i/ )
#    do
#        echo -e "\n==> Processing docker image $i:$j"
#        make -f ../Makefile image-build TARGET_DIR=$i DOCKERFILE=$j
#    done
#done

build_all () {
    for i in $(ls -d */ | tr '/' ' ')
    do
        for j in $(ls $i/ )
        do
            echo -e "\n==> Processing docker image $i:$j"
            make -f ../Makefile image-build TARGET_DIR=$i DOCKERFILE=$j
        done
    done
}

push_all () {
    for i in $(ls -d */ | tr '/' ' ')
    do
        for j in $(ls $i/ )
        do
            echo -e "\n==> Processing docker image $i:$j"
            make -f ../Makefile hub-push TARGET_DIR=$i DOCKERFILE=$j
        done
    done
}

(( BUILD )) && build_all
(( PUSH )) && push_all
