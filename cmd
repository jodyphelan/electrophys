awk '{print "9b320_"$1".abf"}' samples.txt  > files
while read line; do find /media/jody/ArchieDisk/PhD/Results/Electrophysiology/ -name $line; done < files  > filenames.txt
while read line; do python analyseABF.py $line; done < filenames.txt

