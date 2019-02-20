for file in *POSscores
do
	mv "$file" "${file%.txt.out.txt POSscores}.POS.txt"
done
