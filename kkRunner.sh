#!/bin/bash

rootDir=$1
pattern=$2
#echo $pattern
minClu="20"
maxClu="50"
cd $rootDir
cd "FD"

for i in $pattern;do
	echo $i
	KlustaKwik ${i%%.*} ${i##*.} -Verbose 0 -UseDistributional 0 -MinClusters $minClu -MaxClusters $maxClu -MaxPossibleClusters $maxClu &  
	done
	wait
echo KK\'ing is Done!!!
#mail -s "KlustaKwicking is done" chenani@bio.lmu.de <<< "..........."
