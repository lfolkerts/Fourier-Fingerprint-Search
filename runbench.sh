#!/bin/bash
BENMARK_DIR="./benchmarks/FabWave/"
NUM_CATEGORIES=$(find ./benchmarks/FabWave/* -maxdepth 1 -type d | wc -l)
I_FIL=1
I_CAT=1
I_CNT=0
CUM_SCORE1=0
CUM_SCORE2=0
STL_FIL=$(sed $I_FIL'!d' "benchmarks/FabWave/files.txt")	
PSTL_FIL=$STL_FIL
export STL_FIL PSTL_FIL
while [ $I_FIL -lt 3002 ]
do
	STL_FIL=$(sed $I_FIL'!d' "benchmarks/FabWave/files.txt")	
	SAME_PATH=$(python -c 'import score ; \
		import os ; \
		score.bash_same_path(os.environ["STL_FIL"], os.environ["PSTL_FIL"])')
	if [ $SAME_PATH -eq "0" ]
	then
		I_CAT=1
		PSTL_FIL=$STL_FIL
	elif [ $I_CAT -gt 3 ]
	then
		I_FIL=$[$I_FIL + 1]
		continue
	fi
	
	echo $I_FIL $I_CAT $STL_FIL
	RESULT=$(python main.py --mode search --stl $STL_FIL --N 2 --neighborhoods --print_fine_grained | grep "Score")
	SCORE1=$(echo $RESULT | grep -o "Score: [01].[0-9]*" | head -1 | sed 's/.*://')
	SCORE2=$(echo $RESULT | sed 's/.*://')

	CUM_SCORE1=$(echo "$CUM_SCORE1 + $SCORE1" | bc -l)
	CUM_SCORE2=$(echo "$CUM_SCORE2 + $SCORE2" | bc -l)
	I_FIL=$[$I_FIL + 1]
	I_CAT=$[$I_CAT + 1]
	I_CNT=$[$I_CNT + 1]
done


CUM_SCORE1=$(echo "$CUM_SCORE1 / $I_CNT" | bc -l)
CUM_SCORE2=$(echo "$CUM_SCORE2 / $I_CNT" | bc -l)
echo "Signature Match Cumlative Score:" $CUM_SCORE1
echo "Neighborhood Match Cumlative Score:" $CUM_SCORE2
