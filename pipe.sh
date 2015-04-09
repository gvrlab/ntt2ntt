#!/bin/bash

pwd=$(pwd)

rootDir="$1"
cd $rootDir

folder="mScripts"
#echo "$folder"

if [ $# -ne 1 ]
then
	echo "Usage: $0 {dir-name}"
	exit 1
fi
 
if [ -d "$folder" ]
then
	echo "$folder directory  exists!"
	cd $folder
else
	echo "Creating $folder to write scripts!"
	mkdir "$folder"
fi
cd $pwd

python ./scriptWriter.py $rootDir
cd $rootDir
cd $folder

chmod +x features.sh
./features.sh
cd $pwd
bash kkRunner.sh "$rootDir" $rootDir"FD/*.fet.*"
python ./nttWriter.py $rootDir

