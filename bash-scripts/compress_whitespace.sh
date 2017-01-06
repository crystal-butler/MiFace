#!bash

for file in *
do
	tr -s " " < "$file" > temp.txt
	mv temp.txt ../Trial2_Cosine_scoresOnly/"$file"
done
