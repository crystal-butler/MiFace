for file in *.txt
do 
	awk '{if($3 > 400) $3 = 400; print}' $file > temp.txt
	mv temp.txt $file
done