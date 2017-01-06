for file in *.scores.txt
do
	mv "$file" "${file%.scores.txt}"
done