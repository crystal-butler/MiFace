for file in *;
	do awk '{if ($1 ~ /[a-z]/) print FILENAME " " $1;}' $file >> ../badLabels.txt;
done