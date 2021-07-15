for ((k=1;k<200;k +=10))
do
	echo $k
    python3 genetic_alg.py text.txt 15 --key=faciliterebbero --npop=$k

done
