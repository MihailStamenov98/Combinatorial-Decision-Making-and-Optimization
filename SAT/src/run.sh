!/bin/sh
for j in {1..20};
do 
       /mnt/c/Users/mpsta/AppData/Local/Programs/Python/Python310/python.exe sat.py -i $j -e 2 -d -r;
       wait;
       echo $j;
       sleep 1;
done