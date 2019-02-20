for file in *.atxt
do 
	awk '{$1 /= 400; print}' $file > temp.txt
	mv temp.txt $file
done